from __future__ import annotations

from typing import Any, Dict, Optional

from eis1600.helper.markdown_patterns import MIU_HEADER
from eis1600.miu.HeadingTracker import HeadingTracker


class YAMLHandler:
    """A class to take care of the MIU YAML Headers

    :param Dict yml: the YAML header as a dict, optional.
    :ivar Literal['NOT REVIEWED', 'REVIEWED'] reviewed: Indicates if the file has manually been reviewed, defaults to
    'NOT REVIEWED'.
    :ivar str reviewer: Initials of the reviewer if the file was already manually reviewed, defaults to None.
    :ivar HeadingTracker headings: HeadingTracker returned by the get_curr_state method of the HeaderTracker.
    :ivar List[str] dates_headings: List of dates tags contained in headings.
    :ivar List[int] dates: List of dates contained in the text.
    :ivar Dict onomstics: contains onomastic elements by category.
    :ivar str category: String categorising the type of the entry, bio, chr, dict, etc.
    """

    @staticmethod
    def __parse_yml_val(val: str) -> Any:
        if val.isdigit():
            return int(val)
        elif val == 'True':
            return True
        elif val == 'False':
            return False
        elif val == 'None' or val == '':
            return None
        elif val.startswith(('\'', '"')):
            return val.strip('\'"')
        elif val.startswith('['):
            # List - no comma allowed in strings, it is used as the separator!
            raw_val_list = val.strip('[]')
            if raw_val_list.startswith('(') and raw_val_list.endswith(')'):
                # List of tuples
                val_list = raw_val_list.strip('()').split('), (')
                values = []
                for v in val_list:
                    t = v.split(', ')
                    values.append((YAMLHandler.__parse_yml_val(t[0]), YAMLHandler.__parse_yml_val(t[1])))
            else:
                # List of other values
                val_list = raw_val_list.split(', ')
                values = [YAMLHandler.__parse_yml_val(v) for v in val_list]
            return values
        else:
            return val

    @staticmethod
    def __parse_yml(yml_str: str) -> Dict:
        yml = {}
        level = []
        dict_elem = {}
        for line in yml_str.splitlines():
            if not line.startswith('#'):
                intend = (len(line) - len(line.lstrip())) / 4
                key_val = line.split(':')
                key = key_val[0].strip(' -')
                val = ':'.join(key_val[1:]).strip()

                if intend < len(level):
                    yml[level[0]] = dict_elem
                    dict_elem = {}
                    level.pop()

                if intend and intend == len(level):
                    dict_elem[key] = YAMLHandler.__parse_yml_val(val)
                elif val == '':
                    dict_elem = {}
                    level.append(key)
                else:
                    yml[key] = YAMLHandler.__parse_yml_val(val)

        if len(level):
            yml[level[0]] = dict_elem

        return yml

    def __init__(self, yml: Optional[Dict] = None) -> None:
        self.reviewed = 'NOT REVIEWED'
        self.reviewer = None
        self.headings = None
        self.dates_headings = None
        self.dates = None
        self.onomastics = None
        self.category = None
        self.ambigious_toponyms = False

        if yml:
            for key, val in yml.items():
                if key == 'headings':
                    val = HeadingTracker(val)
                self.__setattr__(key, val)

    @classmethod
    def from_yml_str(cls, yml_str: str) -> YAMLHandler:
        """Return instance with attr set from the yml_str."""
        return cls(YAMLHandler.__parse_yml(yml_str))

    def set_category(self, category: str) -> None:
        self.category = category

    def set_ambigious_toponyms(self) -> None:
        self.ambigious_toponyms = True

    def set_headings(self, headings: HeadingTracker) -> None:
        self.headings = headings

    def unset_reviewed(self) -> None:
        self.reviewed = 'NOT REVIEWED'
        self.reviewer = None

    def get_yamlfied(self) -> str:
        yaml_str = MIU_HEADER + 'Begin#\n\n'
        for key, val in vars(self).items():
            if key == 'category' and val is not None:
                yaml_str += key + '    : \'' + val + '\'\n'
            elif isinstance(val, dict):
                yaml_str += key + '    :\n'
                for key2, val2 in val.items():
                    yaml_str += '    - ' + key2 + '  : ' + str(val2) + '\n'
            elif val is not None:
                yaml_str += key + '    : ' + str(val) + '\n'
        yaml_str += '\n' + MIU_HEADER + 'End#\n\n'

        return yaml_str

    def to_json(self) -> Dict:
        json_dict = {}
        for key, val in vars(self).items():
            if val is not None:
                #if key == 'dates':
                #    val = [elem for elem in val if isinstance(elem, (str, int))]
                #    json_dict[key] = [{'str': d_str, 'num': d_num} for d_str, d_num in val]
                json_dict[key] = val
        return json_dict

    def is_bio(self) -> bool:
        return self.category == '$' or self.category == '$$'

    def is_reviewed(self) -> bool:
        return self.reviewed.startswith('REVIEWED')

    def add_date(self, date: int) -> None:
        if self.dates:
            if date not in self.dates:
                self.dates.append(date)
        else:
            self.dates = [date]

    def add_date_headings(self, date: int) -> None:
        if self.dates_headings:
            if date not in self.dates_headings:
                self.dates_headings.append(date)
        else:
            self.dates_headings = [date]

    def add_tagged_entities(self, entities_dict: dict) -> None:
        for key, val in entities_dict.items():
            self.__setattr__(key, val)

    def __setitem__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return self.get_yamlfied()

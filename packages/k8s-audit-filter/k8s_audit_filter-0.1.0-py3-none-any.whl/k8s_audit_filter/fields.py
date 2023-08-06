from typing import List, Union


class BaseField:
    __slots__ = ("name", "value")

    def __init__(self, value: Union[str, List[str], None]):
        self.name: Union[str, None] = None
        self.value: Union[str, List[str], None] = value

    def __eq__(self, other):
        return self.name == other.name and self.value == other.value

    def check_match(self, target: dict) -> bool:
        if target[self.name] == self.value:
            return True
        return False


class LevelField(BaseField):
    def __init__(self, value: Union[str, None]):
        super().__init__(value)
        self.name: Union[str, None] = "level"
        if value is None:
            raise ValueError("Invalid value for level field")
        self.value = value


class VerbsField(BaseField):
    def __init__(self, value: List[str]):
        self.name = "verb"
        self.value: List[str] = value

    def check_match(self, target: dict) -> bool:
        if target[self.name] in self.value:
            return True
        return False


class UsersField(BaseField):
    def __init__(self, value: List[str]):
        self.name = "user"
        self.value: List[str] = value

    def check_match(self, target: dict) -> bool:
        if target[self.name]["username"] in self.value:
            return True
        return False


class UserGroupsField(BaseField):
    def __init__(self, value: List[str]):
        self.name = "user"
        self.value: List[str] = value

    def check_match(self, target: dict) -> bool:
        for group in target[self.name]["groups"]:
            if group in self.value:
                return True
        return False


class FieldException(Exception):
    pass


class FieldFactory:
    field_mapping = {
        "level": LevelField,
        "verbs": VerbsField,
        "users": UsersField,
        "userGroups": UserGroupsField,
    }

    @classmethod
    def create(cls, fields: dict):
        result = []
        for key, vale in fields.items():
            if key in cls.field_mapping:
                result.append(cls.field_mapping[key](vale))
                continue
            raise FieldException(f"Invalid field {key} for Rule")
        return result

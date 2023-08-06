from abc import ABC

from .fields import FieldFactory


class Rule(ABC):
    def __init__(self, fields: dict):
        self.as_dict = fields
        self.fields = FieldFactory.create(fields)

    def __str__(self):
        return f"{self.__class__.__qualname__}: {self.as_dict}"

    def __eq__(self, other):
        return self.fields == other.fields

    def check_rule(self, instance: dict) -> bool:
        raise NotImplementedError


class IncludeRule(Rule):
    def check_rule(self, instance: dict) -> bool:
        for field in self.fields:
            if not field.check_match(instance):
                return False
        return True


class ExcludeRule(Rule):
    def check_rule(self, instance: dict) -> bool:
        for field in self.fields:
            if field.check_match(instance):
                return False
        return True


class RuleException(Exception):
    pass


class RuleFactory:
    rule_mapping = {
        "include": IncludeRule,
        "exclude": ExcludeRule,
    }

    @classmethod
    def create(cls, rule: dict):
        # check if rule has level field
        if "level" not in rule:
            raise RuleException("Invalid rule, missing level")
        if rule["level"] is None:
            del rule["level"]
            return cls.rule_mapping["exclude"](rule)
        return cls.rule_mapping["include"](rule)

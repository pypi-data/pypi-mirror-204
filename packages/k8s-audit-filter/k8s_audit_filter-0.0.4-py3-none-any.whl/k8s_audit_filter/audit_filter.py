from typing import Union

import yaml

from .rules import RuleFactory


class AuditFilterException(Exception):
    pass


class AuditFilter:
    def __init__(self, config: Union[dict, str, None] = None):
        if isinstance(config, str) and ("yaml" in config or "yml" in config):
            with open(config) as f:
                policy = yaml.safe_load(f)
            if "apiVersion" not in policy or policy["apiVersion"] != "audit.k8s.io/v1":
                raise AuditFilterException(
                    "Invalid policy, missing version or version does not match 'audit.k8s.io/v1'"
                )
            if "kind" not in policy or policy["kind"] != "Policy":
                raise AuditFilterException("Invalid policy, missing kind or kind does not match 'Policy'")
            self.rules = [RuleFactory.create(rule) for rule in policy["rules"]]
        elif isinstance(config, dict):
            self.rules = [RuleFactory.create(rule) for rule in config["rules"]]
        elif config is None:
            self.rules = []
        else:
            raise TypeError("Invalid config")

    def filter(self, log_line: dict) -> bool:
        if not self.rules:
            return True  # no rules, no filter
        for rule in self.rules:
            if rule.check_rule(log_line):
                return True
        return False

    def add_rule(self, rule: dict):
        rule = RuleFactory.create(rule)
        self.rules.append(rule)

    def remove_rule(self, rule: dict):
        rule = RuleFactory.create(rule)
        self.rules.remove(rule)

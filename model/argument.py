from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Rule:
    rule: Optional[Dict]
    value: list

    @staticmethod
    def from_dict(rule_info: dict)-> "Rule":
        value = []
        if(type(rule_info["value"]) == str):
            value.append(rule_info["value"])
        else:
            value.extend(rule_info["value"])
        return Rule(
            rule=rule_info["rules"],
            value= value
        )



from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class Rule:
    rule: Optional[List[Dict]]
    value: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(rule_info: dict)-> "Rule":
        
        return Rule(
            rule=rule_info.get("rules", []),
            value= [rule_info["value"]] if isinstance(rule_info["value"], str) else rule_info["value"]
        )



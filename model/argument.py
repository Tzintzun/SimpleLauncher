from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class Rule:
    """
    Regla de configuración para lanzar el juego.
    Attributes:
        rule (Optional[List[Dict]]): Lista de diccionarios que contiene la regla.
        value (List[str]): Valor en caso de que la regla se cumpla.
    """
    rule: Optional[List[Dict]]
    value: List[str] = field(default_factory=list)

    @staticmethod
    def from_dict(rule_info: dict)-> "Rule":
        """
        Convierte un diccionario en Rule.
        Args:
            reule_info (dict):
        
        Returns:
            Rule:
        """
        return Rule(
            rule=rule_info.get("rules", []),
            value= [rule_info["value"]] if isinstance(rule_info["value"], str) else rule_info["value"]
        )



from dataclasses import dataclass, field
from typing import Optional, Dict, List

__docformat__ = "Google-style"

@dataclass
class Rule:
    """
    Regla de configuración para lanzar el juego.
    """
    rule: Optional[List[Dict]]
    """Lista de reglas"""
    value: List[str] = field(default_factory=list)
    """Lista de valores para las reglas"""

    @staticmethod
    def from_dict(rule_info: dict)-> "Rule":
        """
        Convierte un diccionario en Rule.

        Args:
            reule_info (dict):
        
        Returns:
            Rule
        """
        return Rule(
            rule=rule_info.get("rules", []),
            value= [rule_info["value"]] if isinstance(rule_info["value"], str) else rule_info["value"]
        )



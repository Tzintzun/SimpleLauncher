from dataclasses import dataclass

__docformat__ = "Google-style"

@dataclass
class JavaVersion:
    """
    Contiene la informacion de una version de java
    """
    component: str
    """Componente de java que se recomienda usar."""
    major_version: int
    """Version de java que se debe de usar."""

    @staticmethod
    def from_dict(java_version_dic: dict) -> "JavaVersion":
        """
        Obtiene un JavaVersion apartir de un diccionario.

        Args:

            java_version_dict (dict)

        Returns:

            JavaVersion
        """
        return JavaVersion(component=java_version_dic["component"], major_version=java_version_dic["majorVersion"])
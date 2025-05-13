from dataclasses import dataclass


@dataclass
class JavaVersion:
    """
    Contiene la informacion de una version de java
    Attributes:
        component (str): componente de java que se recomienda usar.
        major_version (str): version de java que se debe de usar.
    """
    component: str
    major_version: int

    @staticmethod
    def from_dict(java_version_dic: dict) -> "JavaVersion":
        """
        Obtiene un JavaVersion apartir de un diccionario.
        Args:
            java_version_dict:

        Returns:
            JavaVersion:
        """
        return JavaVersion(component=java_version_dic["component"], major_version=java_version_dic["majorVersion"])
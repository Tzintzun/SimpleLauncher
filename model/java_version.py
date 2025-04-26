from dataclasses import dataclass


@dataclass
class JavaVersion:
    component: str
    major_version: int

    @staticmethod
    def from_dict(java_version_dic: dict) -> "JavaVersion":
        return JavaVersion(component=java_version_dic["component"], major_version=java_version_dic["majorVersion"])
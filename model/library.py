from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class LibraryDownloads:
    artifact: Optional[Dict]
    classifiers: Optional[Dict]

@dataclass
class Library:
    name: str
    downloads: Optional[LibraryDownloads]
    rules: Optional[list]
    natives: Optional[Dict]

    @staticmethod
    def from_dict(data:dict) -> "Library":
        downloads_data = data.get("downloads")
        downloads = (LibraryDownloads(
            artifact= downloads_data.get("artifact"),
            classifiers= downloads_data.get("classifiers")
            )if downloads_data else None
        ) 
        return Library(
            name=data["name"],
            downloads=downloads,
            rules=data.get("rules"),
            natives=data.get("natives")
        )
    
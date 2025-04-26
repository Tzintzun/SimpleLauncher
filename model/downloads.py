from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class DownloadObject:
    sha1: str
    size: int
    url: str

    @staticmethod
    def from_dict(download_data: dict) -> "DownloadObject":
        return DownloadObject(
            sha1= download_data["sha1"],
            size= download_data["size"],
            url= download_data["url"]
        )

@dataclass
class Downloads:
    objects: Optional[Dict[str, DownloadObject]]

    @staticmethod
    def from_dict(downloads: dict) -> "Downloads":
        return Downloads(
            objects={key: DownloadObject(**value)
                     for key, value in downloads.items()}   if downloads else {}
        )
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

@dataclass
class VersionInfo:
    id: str
    type_version: str
    url: str
    time_version: datetime
    release_time: datetime

    @staticmethod
    def from_dict(version_info:dict) ->"VersionInfo":
        time_version = datetime.fromisoformat(version_info["time"]) if version_info["time"] else datetime.now()
        release_time = datetime.fromisoformat(version_info["releaseTime"]) if version_info["releaseTime	"] else datetime.now()
        return VersionInfo(
            id=version_info["id"],
            type_version= version_info["type"],
            url=version_info["url"],
            time_version=time_version,
            release_time=release_time
        )

@dataclass
class VersionManifest:
    release_id: str
    snapshot: str
    versions: List[VersionInfo]
    versions_dcit: Dict[str, VersionInfo] = field(default_factory=dict)

    @staticmethod
    def form_dict(version_manifest:dict) -> "VersionManifest":
        versions = [VersionInfo.from_dict(version) for version in version_manifest.get("versions", {})]
        versions_dict = {version.id : version
                         for version in versions}
        latest_versions = version_manifest.get("latest",{})
        return VersionManifest(
            release_id=latest_versions.get("release", ""),
            snapshot=latest_versions.get("snapshot", ""),
            versions=versions,
            versions_dcit=versions_dict
        )
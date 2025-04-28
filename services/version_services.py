from model.version_manifests import VersionManifest
from services.download_service import download_json
from launcher.config import get_version_manifest_url


VERSIONS_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest.json"


def fetch_version_manifest() -> "VersionManifest | None":
    version_manifest = download_json(get_version_manifest_url())

    if version_manifest is None:
        print(f"No se pudo obtener el Manifiesto de versiones de: {VERSIONS_MANIFEST_URL}")
        return None
    
    return VersionManifest.form_dict(version_manifest)
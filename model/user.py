import uuid

__docformat__ = "Google-style"

class User:
    """
    Informacion del usuario
    """
    def __init__(self, user_name: str):
        self.user_name = user_name
        """nombre del uasuario"""
        self.user_uuid = str( uuid.uuid3(uuid.NAMESPACE_DNS, f"OfflinePlayer:{self.user_name}"))
        """id del usuario, necesario para jugar en linea."""
        self.access_token = str(uuid.uuid4())
        """token de acceso, se requiere para jugar en servidores online. """
import uuid

class User:
    """
    Informacion del usuario
    Attributes:
        user_name (str): nombre del uasuario
        user_uuid (str): id del usuario, necesario para jugar en linea.
        access_token (str): token de acceso, se requiere para jugar en servidores online. 
    """
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.user_uuid = str( uuid.uuid3(uuid.NAMESPACE_DNS, f"OfflinePlayer:{self.user_name}"))
        self.access_token = str(uuid.uuid4())
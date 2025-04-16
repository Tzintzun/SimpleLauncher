import uuid

class User():

    def __init__(self, user_name: str):
        self.user_name = user_name
        self.user_uuid = str( uuid.uuid3(uuid.NAMESPACE_DNS, f"OfflinePlayer:{self.user_name}"))
        self.access_toke = str(uuid.uuid4())
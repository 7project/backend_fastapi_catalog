
class EntityNotFoundError(Exception):
    def __init__(self, entity_name: str, uid: str):
        super().__init__(f"{entity_name} with UID {uid} not found")

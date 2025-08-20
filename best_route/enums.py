from enum import Enum

class ActionType(str, Enum):
    PICK = "PICK"
    DROP = "DROP"

class Notes(str, Enum):
    DELIVERED = "Delivered"
    WAITED = "Arrived early, waited"
    ON_TIME = "Arrived on/after ready"

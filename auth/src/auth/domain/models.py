"""
Business objects
"""
from enum import Enum


class Role(str, Enum):
    """Role enum.

    This class represents the role of a user.
    """
    ADMIN = "admin"
    USER = "user"


class ServiceStatus(str, Enum):
    """Service status enumeration.

    Attributes:
        ONLINE (str): Service is online.
        OFFLINE (str): Service is offline.
    """

    ONLINE = "online"
    OFFLINE = "offline"

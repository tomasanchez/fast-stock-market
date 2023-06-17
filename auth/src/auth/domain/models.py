"""
Business objects
"""
import uuid
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, UUID4


class ServiceStatus(str, Enum):
    """Service status enumeration.

    Attributes:
        ONLINE (str): Service is online.
        OFFLINE (str): Service is offline.
    """

    ONLINE = "online"
    OFFLINE = "offline"


class BaseEntity(BaseModel):
    """
    Base Model
    """
    id: UUID4 = Field(default_factory=uuid.uuid4, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class User(BaseEntity):
    """User model.
    This class represents a user.
    """
    email: EmailStr
    password: str

"""
Business objects
"""
import datetime
from enum import Enum

from pydantic import BaseModel, Field


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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True


class StockInformation(BaseModel):
    date: datetime.date
    open: float
    higher: float
    lower: float
    close: float


class Quote(BaseModel):
    """
    Quote
    """
    open: float
    higher: float
    lower: float
    price: float
    previous_close: float
    variation: float


class StockData(BaseEntity):
    """
    Stock Data
    """
    symbol: str
    name: str
    type: str
    region: str
    currency: str
    variation: float | None = Field(default=None)
    quote: Quote | None = Field(default=None)
    daily_time_series: list[StockInformation] = Field(default_factory=list)

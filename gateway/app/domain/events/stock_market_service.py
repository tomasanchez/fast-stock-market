"""
Events that may occur in the Stock Market Service.
"""
from pydantic import Field

from app.domain.schemas import CamelCaseModel


class StockMarketQueried(CamelCaseModel):
    """
    The event is raised when the stock market is queried.
    """
    symbol: str = Field(description="The symbol of stock option.", example="BA")
    name: str = Field(description="The name of stock option.", example="Boeing Company")
    type: str = Field(description="The type of stock option.", example="Equity")
    region: str = Field(description="The region of stock option.", example="United States")
    currency: str = Field(description="The currency of stock option.", example="USD")


class QuoteQueried(CamelCaseModel):
    open: float = Field(description="The opening price of the day.", example=220.72)
    higher: float = Field(description="The highest price of the day.", example=223.87)
    lower: float = Field(description="The lowest price of the day.", example=218.975)
    price: float = Field(description="The current price.", example=0.0)
    previous_close: float = Field(description="The previous closing price.", example=219.41)
    variation: float = Field(description="The change in price from last closed price.", example=0.58)


class StockDataRetrieved(StockMarketQueried):
    """
    The event is raised when the stock data is retrieved.
    """
    quote: QuoteQueried = Field(description="Global quote of stock option.")

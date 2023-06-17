"""
Stock Market Service
"""
import abc

from market.adapters.repositories import StockMarketRepository
from market.domain.events import StockMarketQueried, QuoteQueried, StockDataRetrieved
from market.service_layer.errors import StockDataNotFound


class AsyncStockMarketService(abc.ABC):

    @abc.abstractmethod
    async def search_symbol(self, keyword: str) -> list[StockMarketQueried]:
        """
        Searches Stock Data matches for a keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list[StockData] : A list of the Stock Data.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_stock_data(self, symbol: str) -> StockDataRetrieved:
        """
        Gets the Global Quote for a Stock Symbol.

        Args:
            symbol (str): The stock symbol to get time series data for.

        Returns:
            QuoteQueried : The Global Quote for a Stock Symbol.

        Raises:
            StockDataNotFound : If the Stock Data does not exist.
        """
        raise NotImplementedError


class StockMarketProvider(AsyncStockMarketService):

    def __init__(self, repository: StockMarketRepository):
        """
        Provides Stock Market Information.

        Args:
            repository (StockMarketRepository): The Stock Market Repository.
        """
        self._repository = repository

    async def search_symbol(self, keyword: str) -> list[StockMarketQueried]:
        stocks = await self._repository.find_all(keyword=keyword)

        return [StockMarketQueried(**stock.dict()) for stock in stocks]

    async def get_stock_data(self, symbol: str) -> StockDataRetrieved:
        stock = await self._repository.find_by(symbol=symbol)

        if stock is None:
            raise StockDataNotFound(f"Could not find Stock Data with symbol: {symbol}")

        return StockDataRetrieved(**stock.dict())

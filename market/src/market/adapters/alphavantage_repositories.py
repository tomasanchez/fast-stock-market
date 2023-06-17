"""
AlphaVantage API Repositories Implementation.
"""

import aiohttp

from market.adapters.http_client import AsyncHttpClient
from market.adapters.repositories import StockMarketRepository
from market.domain.models import StockInformation, StockData, Quote


def parse_symbol_search(search: dict) -> list[StockData]:
    """
    Parses the symbol search data from the AlphaVantage API.

    Args:
        search (dict): The symbol search data.

    Returns:
        list[StockInformation] : A list of stock information.

    """
    matches = search.get("bestMatches", [])

    return [
        StockData(
            symbol=s["1. symbol"],
            name=s["2. name"],
            type=s["3. type"],
            region=s["4. region"],
            currency=s["8. currency"],
        )
        for s in matches
    ]


def parse_quote(quote: dict) -> Quote | None:
    """
    Parses the quote data from the AlphaVantage API.

    Args:
        quote (dict): The quote data.

    Returns:
        Quote : A quote instance.
    """
    global_quote = quote.get("Global Quote", None)

    return Quote(
        open=global_quote["02. open"],
        higher=global_quote["03. high"],
        lower=global_quote["04. low"],
        price=global_quote["05. price"],
        previous_close=global_quote["08. previous close"],
        variation=global_quote["09. change"],
    ) if global_quote else None


class AlphaVantageAPI:
    """
    API Mixin.
    """

    def __init__(self,
                 http_client: AsyncHttpClient,
                 base_url: str = "https://www.alphavantage.co",
                 api_key: str = "demo"
                 ):
        self._base_url = base_url
        self._api_key = api_key
        self._client = http_client

    async def get_symbol(self, symbol: str) -> dict | None:
        """
        Gets time series data from the repository.

        Args:
            symbol (str): The stock symbol to get time series data for.

        Returns:
            list[StockInformation] : A list of time series stock market information.

        """
        url = f"{self._base_url}/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey={self._api_key}"

        try:
            response = await self._client.get(url)
            data = await response.json()
        except aiohttp.ClientConnectorError as e:
            data = None

        return data

    async def get_global_quote(self, symbol: str) -> dict | None:
        """
        Gets the Global Quote for a Stock Symbol.

        Args:
            symbol (str): The stock symbol to get time series data for.

        Returns:
            list[StockInformation] : A list of time series stock market information.

        """
        url = f"{self._base_url}/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self._api_key}"

        try:
            response = await self._client.get(url)
            data = await response.json()
        except aiohttp.ClientConnectorError as e:
            data = dict()

        return data


class AlphaVantageStockMarketRepository(StockMarketRepository, AlphaVantageAPI):
    """
    AlphaVantageStockMarketRepository implementation.
    """

    async def find_all(self, keyword: str) -> list[StockData]:
        """
        Searches Stock Data matches for a keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list[StockData] : A list of the Stock Data.
        """
        data = await self.get_symbol(keyword)

        return parse_symbol_search(data)

    async def find_by(self, symbol: str) -> StockData | None:
        quote = await self.get_global_quote(symbol)

        if not quote.get('Global Quote', None):
            return None

        best_match = (await self.find_all(symbol))[0]

        best_match.quote = parse_quote(quote)

        return best_match

    async def get_daily_time_series(self, symbol: str, *args, **kwargs) -> list[StockInformation]:
        pass

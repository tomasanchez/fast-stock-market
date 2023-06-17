"""
FastAPI application dependencies.
"""
from typing import Annotated

from fastapi import Depends

from market.adapters.alphavantage_repositories import AlphaVantageStockMarketRepository
from market.adapters.http_client import AsyncHttpClient, AiohttpClient
from market.adapters.repositories import StockMarketRepository
from market.service_layer.stock_market import AsyncStockMarketService, StockMarketProvider
from market.settings.app_settings import ApplicationSettings

async_http_client: AsyncHttpClient | None = None


def get_async_http_client() -> AsyncHttpClient:
    """
    Get AsyncHttpClient instance.

    Returns:
        AsyncHttpClient: AsyncHttpClient instance.
    """
    global async_http_client

    if async_http_client is None:
        async_http_client = AiohttpClient()

    return async_http_client


AsyncHttpClientDependency = Annotated[AsyncHttpClient, Depends(get_async_http_client)]

market_repository: StockMarketRepository | None = None


def get_market_repository() -> StockMarketRepository:
    """
    Get StockMarketRepository instance.

    Returns:
        StockMarketRepository: StockMarketRepository instance.
    """
    global market_repository

    api_key = ApplicationSettings().ALPHA_VANTAGE_API_KEY

    if market_repository is None:
        market_repository = AlphaVantageStockMarketRepository(http_client=get_async_http_client(), api_key=api_key)

    return market_repository


MarketRepositoryDependency = Annotated[StockMarketRepository, Depends(get_market_repository)]

stock_market_service: AsyncStockMarketService | None = None


def get_stock_market_service(repository: MarketRepositoryDependency) -> AsyncStockMarketService:
    """
    Injects a AsyncStockMarketService instance.
    """
    global stock_market_service

    if stock_market_service is None:
        stock_market_service = StockMarketProvider(repository=repository)

    return stock_market_service


StockMarketDependency = Annotated[AsyncStockMarketService, Depends(get_stock_market_service)]

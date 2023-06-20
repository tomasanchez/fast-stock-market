"""
Stock Market Service Gateway Entry Point.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, status, Query, Path

from app.adapters.network import gateway
from app.dependencies import ServiceProvider, AsyncHttpClientDependency
from app.domain.events.stock_market_service import StockMarketQueried, StockDataRetrieved
from app.domain.schemas import ResponseModels, ResponseModel
from app.middleware import AuthMiddleware
from app.service_layer.gateway import get_service, api_v1_url, verify_status

router = APIRouter(prefix="/stocks")


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="Queries Stock Data matches for a keyword.",
            tags=["Queries"],
            )
async def find_stock_market_matches(
        keyword: Annotated[str, Query(title="Keyword", description="Keyword to search for.", example="BA")],
        services: ServiceProvider,
        user: AuthMiddleware,
        client: AsyncHttpClientDependency,
) -> ResponseModels[StockMarketQueried]:
    """
    Retrieves information of Stock Data which best matches a keyword.
    """

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="Stock Market", services=services)).base_url,
        path=f"{api_v1_url}/stocks",
        client=client,
        method="GET",
        query_params=dict(keyword=keyword),
    )

    verify_status(response=service_response, status_code=status_code)

    logging.info(
        f"Data Retrieved: Stock Market Queried by User(email={user.email})"
        f" with Keyword={keyword} got {len(service_response.get('data', []))} results.")

    return ResponseModels[StockMarketQueried](**service_response)


@router.get("/{symbol}",
            status_code=status.HTTP_200_OK,
            summary="Gets the Global Quote for a Stock Symbol.",
            tags=["Queries"],
            )
async def find_stock_symbol(
        symbol: Annotated[str, Path(description="Stock Symbol to search for.", example="BA")],
        services: ServiceProvider,
        user: AuthMiddleware,
        client: AsyncHttpClientDependency,
) -> ResponseModel[StockDataRetrieved]:
    """
    Retrieves information of Stock Data which best matches a keyword.
    """

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="Stock Market", services=services)).base_url,
        path=f"{api_v1_url}/stocks/{symbol}",
        client=client,
        method="GET",
    )

    verify_status(response=service_response, status_code=status_code)

    logging.info(f"Data Retrieved: Stock Market Queried by User(email={user.email}) for Symbol={symbol}.")

    return ResponseModel[StockDataRetrieved](**service_response)

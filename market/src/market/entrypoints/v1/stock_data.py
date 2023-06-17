from fastapi import APIRouter, status, HTTPException

from market.dependencies import StockMarketDependency
from market.domain.events import StockMarketQueried, StockDataRetrieved
from market.domain.schemas import ResponseModels, ResponseModel
from market.service_layer.errors import StockDataNotFound

router = APIRouter(prefix="/stocks")


@router.get("/",
            status_code=status.HTTP_200_OK,
            summary="Queries Stock Data matches for a keyword.",
            tags=["Queries"]
            )
async def find_stock_market_matches(keyword: str,
                                    provider: StockMarketDependency,
                                    ) -> ResponseModels[StockMarketQueried]:
    """
    Retrieves information of Stock Data which best matches a keyword.
    """
    stocks = await provider.search_symbol(keyword=keyword)

    return ResponseModels[StockMarketQueried](data=stocks)


@router.get("/{symbol}",
            status_code=status.HTTP_200_OK,
            summary="Gets the Global Quote for a Stock Symbol.",
            tags=["Queries"]
            )
async def get_symbol(symbol: str,
                     provider: StockMarketDependency,
                     ) -> ResponseModel[StockDataRetrieved]:
    try:
        stock = await provider.get_stock_data(symbol=symbol)
    except StockDataNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    return ResponseModel[StockDataRetrieved](data=stock)

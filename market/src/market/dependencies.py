"""
FastAPI application dependencies.
"""
from typing import Annotated

from fastapi import Depends

from market.adapters.http_client import AsyncHttpClient, AiohttpClient

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

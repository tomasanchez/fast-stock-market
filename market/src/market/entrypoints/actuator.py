"""
Actuator Entry Point.
"""
from fastapi import APIRouter, status, HTTPException
from starlette.responses import RedirectResponse

from market.domain.events import StatusChecked, ReadinessChecked
from market.domain.models import ServiceStatus
from market.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/readiness",
            status_code=status.HTTP_200_OK,
            summary="Readiness probe.")
async def readiness() -> ResponseModel[ReadinessChecked]:
    """
    Checks if the service is ready to accept requests.
    """
    services_status: list[StatusChecked] = list()

    readiness_checked = ReadinessChecked(status=ServiceStatus.ONLINE)

    if any([service for service in services_status if service.status == ServiceStatus.OFFLINE]):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=readiness_checked.dict())

    return ResponseModel(data=readiness_checked)


@router.get("/liveliness",
            status_code=status.HTTP_200_OK,
            summary="Liveliness probe.")
async def liveliness() -> ResponseModel[StatusChecked]:
    """
    Checks if the service is up and running.
    """
    return ResponseModel(data=StatusChecked(name="api-gateway", status=ServiceStatus.ONLINE))


@router.get(
    "/",
    include_in_schema=False,
    status_code=status.HTTP_301_MOVED_PERMANENTLY,
)
def root_redirect():
    """
    Redirects the root path to the docs.
    """
    return RedirectResponse(url="/docs", status_code=status.HTTP_301_MOVED_PERMANENTLY)

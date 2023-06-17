"""
Actuator Entry Point.
"""
from fastapi import APIRouter, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from starlette.responses import RedirectResponse

from auth.dependencies import ClientFactoryDependency
from auth.domain.events import StatusChecked, ReadinessChecked
from auth.domain.models import ServiceStatus
from auth.domain.schemas import ResponseModel

router = APIRouter(tags=["Actuator"])


@router.get("/readiness",
            status_code=status.HTTP_200_OK,
            summary="Readiness probe.")
async def readiness(mongo_factory: ClientFactoryDependency) -> ResponseModel[ReadinessChecked]:
    """
    Checks if the service is ready to accept requests.
    """
    mongo_status = await _ping_database(client=mongo_factory())
    services_status: list[StatusChecked] = [mongo_status]

    readiness_checked = ReadinessChecked(status=ServiceStatus.ONLINE, services=services_status)

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


####################################################################################################
# Internal Methods
####################################################################################################

async def _ping_database(client: AsyncIOMotorClient) -> StatusChecked:
    """
    Pings the database.

    Args:
        client (MongoClient): The database client.

    Returns:
        StatusChecked: The status of the database.
    """
    service_status = StatusChecked(name="mongodb", status=ServiceStatus.ONLINE)

    try:
        await client.admin.command("ping")
    except ConnectionFailure as e:
        service_status.status = ServiceStatus.OFFLINE
        service_status.detail = str(e)

    return service_status

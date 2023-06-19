"""
Entry points for the Auth service.
"""
from typing import Annotated

from fastapi import APIRouter, Path, Query, Request, Response
from pydantic import UUID4
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.adapters.network import gateway
from app.dependencies import AsyncHttpClientDependency, ServiceProvider
from app.domain.commands.auth_service import AuthenticateUser, RegisterUser
from app.domain.events.auth_service import TokenGenerated, UserAuthenticated, UserCreated
from app.domain.schemas import ResponseModel, ResponseModels
from app.middleware import AuthMiddleware
from app.service_layer.gateway import api_v1_url, get_service, get_users, verify_status
from app.utils.logging import Logger

router = APIRouter()

UsersQuery = Annotated[
    str | None, Query(description="A list of comma-separated usernames.", example="johndoe, other", alias="users")]

logger = Logger().get_logger()


@router.get("/users",
            status_code=HTTP_200_OK,
            summary="Find all users",
            tags=["Queries"]
            )
async def query_users(
        services: ServiceProvider,
        client: AsyncHttpClientDependency) -> ResponseModels[UserCreated]:
    """
    Retrieves users from the Database.
    """

    logger.info("Users Queried.")

    service = await get_service(service_name="auth", services=services)

    response, code = await get_users(service=service, client=client)

    verify_status(response=response, status_code=code)

    return ResponseModels[UserCreated](**response)


@router.get("/users/{user_id}",
            status_code=HTTP_200_OK,
            summary="Find user by ID",
            tags=["Queries"]
            )
async def query_user_by_id(
        user_id: Annotated[UUID4, Path(description="The user's UUID.", example="e7b4d6c0-0b1e-4e1a-8b0a-2b0c0f0c1e1e")],
        services: ServiceProvider,
        client: AsyncHttpClientDependency, ) -> ResponseModel[UserCreated]:
    """
    Retrieves a specific user from the Database.
    """

    service = await get_service(service_name="auth", services=services)

    response, code = await gateway(service_url=service.base_url, path=f"{api_v1_url}/users/{user_id}/",
                                   client=client, method="GET")

    verify_status(response=response, status_code=code)

    logger.info(f"User {user_id} queried.")

    return ResponseModel[UserCreated](**response)


@router.post(
    "/users",
    status_code=HTTP_201_CREATED,
    summary="Command to register a new user",
    tags=["Commands"]
)
async def register(command: RegisterUser,
                   services: ServiceProvider,
                   client: AsyncHttpClientDependency,
                   request: Request,
                   response: Response):
    """
    Register a new user.
    """

    service_response, status_code = await gateway(
        service_url=(await get_service(service_name="auth", services=services)).base_url,
        path=f"{api_v1_url}/users/",
        client=client,
        method="POST",
        request_body=command.json()
    )

    verify_status(response=service_response, status_code=status_code, status_codes=[HTTP_201_CREATED])

    response_body = ResponseModel[UserCreated](**service_response)

    logger.info(f"User {response_body.data.id} created.")

    response.headers["Location"] = f"{request.base_url}api/v1/users/{response_body.data.id}"
    return response_body


@router.post("/auth/token",
             status_code=HTTP_200_OK,
             summary="Command to authenticate a user",
             tags=["Commands"],
             )
async def authenticate(command: AuthenticateUser,
                       services: ServiceProvider,
                       client: AsyncHttpClientDependency) -> ResponseModel[TokenGenerated]:
    """
    Attempts to log in.
    """

    auth_response, status_code = await gateway(
        service_url=(await get_service(service_name="auth", services=services)).base_url,
        path=f"{api_v1_url}/auth/token",
        client=client,
        method="POST",
        request_body=command.json()
    )

    verify_status(response=auth_response, status_code=status_code)

    logger.info(f"User {command.email} authenticated.")

    return ResponseModel[TokenGenerated](**auth_response)


@router.get("/auth/me",
            status_code=HTTP_200_OK,
            summary="Authenticates current user",
            tags=["Queries"],
            )
async def authorize(
        user: AuthMiddleware
) -> ResponseModel[UserAuthenticated]:
    """
    Validates a user token. If valid, retrieves the user information.
    """

    logger.info(f"User {user.id} authorized.")

    return ResponseModel[UserAuthenticated](data=user)

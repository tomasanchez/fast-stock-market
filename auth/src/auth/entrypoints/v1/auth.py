"""
Auth Entrypoints
"""
from fastapi import APIRouter, status, HTTPException

from auth.dependencies import AuthServiceDependency
from auth.domain.commands import AuthenticateUser
from auth.domain.events import TokenGenerated, UserAuthenticated
from auth.domain.schemas import ResponseModel
from auth.middleware import BearerTokenAuth
from auth.service_layer.errors import InvalidCredentialsError

router = APIRouter(prefix="/auth")


@router.post("/token",
             summary="Authenticates a user.",
             tags=["Commands"],
             status_code=status.HTTP_200_OK,
             )
async def authenticate(command: AuthenticateUser,
                       auth_service: AuthServiceDependency,
                       ) -> ResponseModel[TokenGenerated]:
    """
    Produces a JSON Web Token.
    """

    try:
        event = await auth_service.authenticate(username=command.email, password=command.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e

    return ResponseModel(data=event)


@router.get('/me', status_code=status.HTTP_200_OK, tags=["Commands"])
async def me(
        token: BearerTokenAuth,
        auth_service: AuthServiceDependency,
) -> ResponseModel[UserAuthenticated]:
    """
    Authorizes a token, providing the user's information.
    """
    try:
        user = await auth_service.authorize(token.credentials)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return ResponseModel(data=user)

"""
Auth Entrypoints
"""
from fastapi import APIRouter

from auth.domain.commands import AuthenticateUser
from auth.domain.events import TokenGenerated
from auth.domain.schemas import ResponseModel

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/token",
            summary="Generates a JWT token.",
            tags=["Commands"]
            )
async def authenticate(command: AuthenticateUser,
                        
                       ) -> ResponseModel[TokenGenerated]:
    """
    Authenticates a user.
    """
    pass

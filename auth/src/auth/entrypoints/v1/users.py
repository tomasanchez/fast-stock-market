"""
Users entrypoint
"""

from fastapi import APIRouter, status

from auth.dependencies import UserRepositoryDependency
from auth.domain.events import UserCreated
from auth.domain.schemas import ResponseModels

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/",
            status_code=status.HTTP_200_OK,
            tags=["Queries"])
async def query_users(user_repository: UserRepositoryDependency) -> ResponseModels[UserCreated]:
    """
    Retrieves a collection of users from the database.
    """

    users = await user_repository.find_all()

    return ResponseModels[UserCreated](data=[UserCreated(**user) for user in users])

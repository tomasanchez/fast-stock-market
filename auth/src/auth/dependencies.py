from typing import Annotated

from fastapi import Depends

from auth.adapters.repositories import UserRepository
from tests.mocks import InMemoryUserRepository

user_repository: UserRepository | None = None


def get_user_repository() -> UserRepository:
    """
    Injects a user repository.
    """
    global user_repository

    if not user_repository:
        user_repository = InMemoryUserRepository()

    return user_repository


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]

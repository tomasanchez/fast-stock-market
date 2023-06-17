from typing import Generic

from auth.adapters.repositories import T, UserRepository, AsyncRepository
from auth.domain.models import User


class AsyncInMemoryRepository(AsyncRepository, Generic[T]):
    """
    An in-memory repository implementation.
    """

    def __init__(self, data: dict[str, T] | None = None):
        self._data: dict[str, T] = data or dict()

    async def find_all(self, *args, **kwargs) -> list[T]:
        return list(self._data.values())

    async def find_by(self, *args, **kwargs) -> T | None:
        properties = kwargs.keys()
        return next(
            (entity for entity in self._data.values()
             if all(getattr(entity, p) == kwargs[p] for p in properties)),
            None)

    async def save(self, entity: T, *args, **kwargs) -> T:
        self._data[str(entity.id)] = entity
        return entity

    async def delete(self, entity: T, *args, **kwargs) -> None:
        del self._data[str(entity.id)]


class InMemoryUserRepository(AsyncInMemoryRepository[User], UserRepository):
    """
    An in-memory user repository implementation.
    """

    async def find_by_email(self, email: str) -> User | None:
        return await self.find_by(email=email)

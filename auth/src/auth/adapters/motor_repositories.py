"""
Motor Repositories implementation
"""
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from auth.adapters.repositories import AsyncReadOnlyRepository, T, AsyncWriteOnlyRepository, UserRepository
from auth.domain.models import User


class MotorRepositoryMixin:
    """
    Mixin class for motor repositories.
    """

    def __init__(self, client: AsyncIOMotorClient,
                 db_name: str,
                 model_factory: type[T]
                 ):
        """

        Args:
            client: Motor Client
            db_name: Name of the database
        """
        self.collection_name = model_factory.__name__.lower()
        self.collection: AsyncIOMotorCollection = client.get_database(db_name).get_collection(self.collection_name)
        self.model_factory = model_factory


class MotorReadOnlyRepository(AsyncReadOnlyRepository, MotorRepositoryMixin):

    async def find_by(self, *args, **kwargs) -> T | None:
        entry = await self.collection.find_one(kwargs)

        if entry:
            return self.model_factory(**entry)

        return None

    async def find_all(self, *args, **kwargs) -> list[T]:
        entries = self.collection.find(kwargs)
        return [self.model_factory(**entry) async for entry in entries]


class MotorWriteOnlyRepository(AsyncWriteOnlyRepository, MotorRepositoryMixin):

    async def save(self, entity: T, *args, **kwargs) -> T:
        entry = jsonable_encoder(entity)
        await self.collection.update_one({"_id": entity.id}, entry, upsert=True)
        return entity

    async def delete(self, entity: T, *args, **kwargs) -> None:
        await self.collection.delete_one({"_id": entity.id})


class MotorUserRepository(UserRepository, MotorWriteOnlyRepository, MotorReadOnlyRepository):
    """
    Motor User Repository
    """

    def __init__(self, client: AsyncIOMotorClient, db_name: str):
        super().__init__(client, db_name, User)

    async def find_by_email(self, email: str) -> User | None:
        return await super().find_by(email=email)

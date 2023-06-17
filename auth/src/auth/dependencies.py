from typing import Annotated

from fastapi import Depends

from auth.adapters.db import ClientFactory
from auth.adapters.motor_repositories import MotorUserRepository
from auth.adapters.repositories import UserRepository
from auth.service_layer.password_encoder import PasswordEncoder, BcryptPasswordEncoder
from auth.service_layer.register import AsyncRegisterService, SimpleRegisterService
from auth.settings.mongo_settings import MongoDbSettings

# ------------------------------- Client Factory ---------------------------
mongo_settings = MongoDbSettings()


def get_client_factory() -> ClientFactory:
    """
    Injects a database client factory.
    """

    return ClientFactory(url=mongo_settings.CLIENT)


ClientFactoryDependency = Annotated[ClientFactory, Depends(get_client_factory)]

# ------------------------------- Repository -------------------------------

user_repository: UserRepository | None = None


def get_user_repository(client_factory: ClientFactoryDependency) -> UserRepository:
    """
    Injects a user repository.
    """
    global user_repository

    if not user_repository:
        user_repository = MotorUserRepository(client=client_factory(), db_name=mongo_settings.DATABASE)

    return user_repository


UserRepositoryDependency = Annotated[UserRepository, Depends(get_user_repository)]

# ------------------------------- Password encoder -------------------------------

password_encoder: PasswordEncoder | None = None


def get_password_encoder() -> PasswordEncoder:
    """
    Injects a password hasher.
    """
    global password_encoder

    if not password_encoder:
        password_encoder = BcryptPasswordEncoder()

    return password_encoder


PasswordEncoderDependency = Annotated[PasswordEncoder, Depends(get_password_encoder)]

# ------------------------------- Register Service  -------------------------------

register_service: AsyncRegisterService | None = None


def get_register_service(repository: UserRepositoryDependency,
                         pw_encoder: PasswordEncoderDependency) -> AsyncRegisterService:
    """
    Injects a register service.
    """
    global register_service

    if not register_service:
        register_service = SimpleRegisterService(user_repository=repository, password_encoder=pw_encoder)

    return register_service


RegisterServiceDependency = Annotated[AsyncRegisterService, Depends(get_register_service)]

"""
This module contains pytest fixtures.
"""
import typing

import pytest
from starlette.testclient import TestClient

from auth.adapters.repositories import UserRepository
from auth.main import app
from auth.service_layer.jwt import JwtService
from auth.service_layer.password_encoder import PasswordEncoder, BcryptPasswordEncoder
from auth.service_layer.register import SimpleRegisterService, AsyncRegisterService
from tests.mocks import InMemoryUserRepository


class DependencyOverrider:
    """
    A context manager for overriding FastAPI dependencies.
    """

    def __init__(
            self, overrides: typing.Mapping[typing.Callable, typing.Callable]
    ) -> None:
        self.overrides = overrides
        self._app = app
        self._old_overrides = {}

    def __enter__(self):
        for dep, new_dep in self.overrides.items():
            if dep in self._app.dependency_overrides:
                # Save existing overrides
                self._old_overrides[dep] = self._app.dependency_overrides[dep]
            self._app.dependency_overrides[dep] = new_dep
        return self

    def __exit__(self, *args: typing.Any) -> None:
        for dep in self.overrides.keys():
            if dep in self._old_overrides:
                # Restore previous overrides
                self._app.dependency_overrides[dep] = self._old_overrides.pop(dep)
            else:
                # Just delete the entry
                del self._app.dependency_overrides[dep]


@pytest.fixture(name="test_client")
def fixture_test_client() -> TestClient:
    """
    Create a test client for the FastAPI application.

    Returns:
        TestClient: A test client for the app.
    """
    return TestClient(app)


@pytest.fixture(name="password_encoder")
def fixture_password_encoder() -> PasswordEncoder:
    """
    Create a password encoder.

    Returns:
        PasswordEncoder: A password encoder.
    """
    return BcryptPasswordEncoder()


@pytest.fixture(name="user_repository")
def fixture_user_repository() -> UserRepository:
    """
    Create a user repository.

    Returns:
        None: A user repository.
    """
    return InMemoryUserRepository()


@pytest.fixture(name="register_service")
def fixture_register_service(
        user_repository: UserRepository,
        password_encoder: PasswordEncoder
) -> AsyncRegisterService:
    """
    Create a register service.

    Returns:
        None: A register service.
    """
    return SimpleRegisterService(user_repository, password_encoder)


@pytest.fixture(name="jwt_service")
def fixture_jwt_service() -> JwtService:
    """
    Create a JWT service.

    Returns:
        JwtService: A JWT service.
    """
    return JwtService()

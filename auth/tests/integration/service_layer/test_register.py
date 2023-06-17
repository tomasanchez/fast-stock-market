"""
Test Register Service
"""
import pytest
from pydantic import EmailStr

from auth.adapters.repositories import UserRepository
from auth.domain.models import User
from auth.service_layer.errors import IllegalUserError
from auth.service_layer.password_encoder import PasswordEncoder
from auth.service_layer.register import AsyncRegisterService


class TestRegisterService:
    """
    Unit test suite for the register in the service layer
    """

    @pytest.mark.asyncio
    async def test_registers_with_encoded_password(self,
                                                   user_repository: UserRepository,
                                                   password_encoder: PasswordEncoder,
                                                   register_service: AsyncRegisterService):
        """
        Test that the register service registers a user with an encoded password
        """

        # Given
        email, password = ("user@mail.com", "password1")

        # When
        registered_user = await register_service.register(username=email, password=password)

        # Then
        password_encoder.verify(password, registered_user.password)

        assert registered_user in await user_repository.find_all()

    @pytest.mark.asyncio
    async def test_cannot_register_with_existing_username(self,
                                                          user_repository: UserRepository,
                                                          register_service: AsyncRegisterService
                                                          ):
        """
        Test that the register service raises an error when an existing username is provided.
        """
        # Given
        existing_email = EmailStr("an@e.mail")
        await user_repository.save(User(email=existing_email, password="password1"))

        email, password = (str(existing_email), "password1")

        # When / Then
        with pytest.raises(IllegalUserError):
            await register_service.register(username=email, password=password)

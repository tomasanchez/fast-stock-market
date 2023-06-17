"""
Register Service
"""
import abc

from pydantic import EmailStr

from auth.adapters.repositories import UserRepository
from auth.domain.models import User
from auth.service_layer.errors import IllegalUserError
from auth.service_layer.password_encoder import PasswordEncoder


class AsyncRegisterService(abc.ABC):
    """
    Abstract Registration Service
    """

    @abc.abstractmethod
    async def register(self, username: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user.

        Raises:
            IllegalUserError: If the username or email is already in use.
        """
        raise NotImplementedError


class SimpleRegisterService(AsyncRegisterService):
    """
    Registration Service
    """

    def __init__(self, user_repository: UserRepository, password_encoder: PasswordEncoder):
        self.user_repository = user_repository
        self.password_encoder = password_encoder

    async def _verify_username(self, username: str):
        """
        Verifies if the username is available.

        Args:
            username (str): The username to verify.

        Raises:
            IllegalUserError: If the username is already in use.
        """
        user = await self.user_repository.find_by_email(email=username)

        if user:
            raise IllegalUserError(f"Email {username} is already in use.")

    async def register(self, username: str, password: str) -> User:
        await self._verify_username(username)

        hashed_password = self.password_encoder.encode(password)

        user = User(email=EmailStr(username), password=hashed_password)

        return await self.user_repository.save(user)

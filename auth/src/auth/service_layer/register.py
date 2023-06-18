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
    async def register(self, username: str, password: str, name: str | None, last_name: str | None) -> User:
        """
        Registers a new user.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            name (str): The name of the user.
            last_name (str): The last name of the user.

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

    async def register(self, username: str,
                       password: str,
                       name: str | None = None,
                       last_name: str | None = None) -> User:
        await self._verify_username(username)

        hashed_password = self.password_encoder.encode(password)

        user = User(email=EmailStr(username), password=hashed_password, name=name, last_name=last_name)

        return await self.user_repository.save(user)

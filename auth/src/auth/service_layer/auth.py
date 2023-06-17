"""Auth Service

Authenticates and authorizes users.
"""
from auth.adapters.repositories import UserRepository
from auth.domain.events import UserAuthenticated, TokenGenerated
from auth.domain.models import User
from auth.service_layer.errors import InvalidCredentialsError
from auth.service_layer.jwt import JwtService
from auth.service_layer.password_encoder import PasswordEncoder


class AuthService:
    """
    Authenticates and authorizes users.
    """

    def __init__(self, user_repository: UserRepository,
                 encoder: PasswordEncoder,
                 jwt_service: JwtService):
        self.user_repository = user_repository
        self.encoder = encoder
        self.jwt_service = jwt_service

    async def _verify_credentials(self, username: str, password: str | None = None) -> UserAuthenticated:
        """
        Verifies if the user exists.

        Args:
            username: An unique username of the user.
            password: The password to verify.

        Returns:
            The user authenticated.

        Raises:
            InvalidCredentialsError: If the user does not exist or the password is invalid.
        """
        user: User = await self.user_repository.find_by(email=username)

        if not user:
            raise InvalidCredentialsError(f"User {username} was not found.")

        if password:
            self.encoder.verify(password, user.password)

        return UserAuthenticated(**user.dict())

    async def authenticate(self, username: str, password: str) -> TokenGenerated:
        """
        Authenticates a user.

        Args:
            username: An unique username of the user.
            password: The password to verify.

        Returns:
            A Json Web Token.

        Raises:
            InvalidCredentialsError: If the user does not exist or the password is invalid.
        """
        user = await self._verify_credentials(username, password)

        return self.jwt_service.get_token(username=user.email, identifier=user.id)

    async def authorize(self, token: str) -> UserAuthenticated:
        """
        Authorizes a user.

        Args:
            token: The token to verify.

        Raises:
            InvalidCredentialsError: If the token is invalid.
        """
        user_token = self.jwt_service.decode_user_token(token)

        user = await self._verify_credentials(user_token.email)

        return user

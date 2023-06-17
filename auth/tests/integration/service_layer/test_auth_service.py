import pytest

from auth.service_layer.errors import InvalidCredentialsError


class TestAuth:

    @pytest.mark.asyncio
    async def test_user_gets_working_token(self, auth_service, register_service):
        """
        Tests that a user can authenticate receiving a usable token.
        """
        # given
        email, password = ("john@do.e", "aGreatPassword")
        await register_service.register(username=email, password=password)
        auth_token = await auth_service.authenticate(username=email, password=password)

        # when
        event = await auth_service.authorize(token=auth_token.token)

        # then
        assert event.email == email

    @pytest.mark.asyncio
    async def test_token_is_not_verifiable(self, auth_service):
        """
        Tests that a user cannot authenticate with invalid credentials.
        """
        # given
        token = "invalid_token"

        # when
        with pytest.raises(InvalidCredentialsError):
            await auth_service.authorize(token=token)

    @pytest.mark.asyncio
    async def test_user_can_not_authenticate_with_invalid_credentials(self, auth_service, register_service):
        """
        Tests that a user cannot authenticate with invalid credentials.
        """
        # given
        email, password = ("john@do.e", "aGreatPassword")
        await register_service.register(username=email, password=password)

        # when
        with pytest.raises(InvalidCredentialsError):
            await auth_service.authenticate(username=email, password="invalid_password")

    @pytest.mark.asyncio
    async def test_user_can_not_authenticate_with_invalid_username(self, auth_service):
        """
        Tests that a user cannot authenticate with invalid username.
        """
        # given
        email, password = ("john@do.e", "aGreatPassword")

        # when
        with pytest.raises(InvalidCredentialsError):
            await auth_service.authenticate(username=email, password=password)

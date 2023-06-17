import uuid

import pytest

from auth.service_layer.errors import InvalidCredentialsError
from auth.service_layer.jwt import JwtService


class TestJwt:

    def test_token_can_be_encoded(self, jwt_service: JwtService):
        """
        Tests that a token can be encoded.
        """
        # given
        username = "test"
        identifier = uuid.uuid4()

        # when
        event = jwt_service.get_token(username=username, identifier=identifier)

        # then
        assert len(event.token) > 0

    def test_token_can_be_decoded(self, jwt_service: JwtService):
        """
        Tests that a token can be decoded.
        """
        # given
        username = "an@e.mail"
        identifier = uuid.uuid4()

        # when
        event = jwt_service.get_token(username=username, identifier=identifier)

        # when
        event_decoded = jwt_service.decode_user_token(event.token)

        # then
        assert event_decoded.email == username
        assert event_decoded.id == identifier

    def test_token_is_invalid(self, jwt_service: JwtService):
        """
        Tests that an invalid token raises an error.
        """
        # given
        token = "invalidToken"

        # when
        with pytest.raises(InvalidCredentialsError):
            jwt_service.decode_user_token(token)

"""Commands
A command represents an intent to change the state of the system, it is a message that requests some action to be taken.

Commands are passed to command handlers, which interpret them and execute
the corresponding actions to produce new events that update the system state.

Commands should be immutable, and their properties should be as minimal as possible.
"""
from pydantic import EmailStr, Field

from auth.domain.schemas import CamelCaseModel

min_length = 8


class RegisterUser(CamelCaseModel):
    """
    Command that represents the intent to register a new user.
    """
    email: EmailStr = Field(description="The user email.", example="john@doe.com")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)


class AuthenticateUser(CamelCaseModel):
    """
    Command that represents the intent to authenticate a user.
    """
    email: EmailStr = Field(description="The user email.", example="john@doe.com")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)

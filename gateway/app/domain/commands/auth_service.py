from pydantic import EmailStr, Field

from app.domain.schemas import CamelCaseModel

min_length = 8


class RegisterUser(CamelCaseModel):
    """
    Command that represents the intent to register a new user.
    """
    email: EmailStr = Field(description="The user email.", example="john@doe.com")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)
    name: str = Field(description="The user first name.", example="John")
    last_name: str = Field(description="The user last name.", example="Doe")


class AuthenticateUser(CamelCaseModel):
    """
    Command that represents the intent to authenticate a user.
    """
    email: EmailStr = Field(description="The user email.", example="john@doe.com")
    password: str = Field(title="Password", description="Login Credential", min_length=min_length)

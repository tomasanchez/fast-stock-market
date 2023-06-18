"""
Events that may occur in the Auth Service.
"""

from pydantic import EmailStr, Field, UUID4

from app.domain.schemas import CamelCaseModel


class UserCreated(CamelCaseModel):
    """
    Event raised when a user is created.
    """

    id: UUID4 = Field(description="The user id.", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
    email: EmailStr = Field(description="The email.", example="john.doe@e.mail")
    first_name: str | None = Field(description="The user first name.", example="John")
    last_name: str | None = Field(description="The user last name.", example="Doe")


class UserAuthenticated(UserCreated):
    """
    Event raised when a user is authenticated.
    """
    pass


class TokenGenerated(CamelCaseModel):
    """
    Event raised when a token is generated.
    """
    token: str = Field(description="A JSON Web Token",
                       example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5kb2UiLCJlbWFpbCI6ImpvaG5kb"
                               "2VAZ21haWwuY29tIiwicm9sZSI6IlVTRVIiLCJleHAiOjE2MjUwMzg4MjB9.5Y2QJ7kx1yD6Bh0jzH2QX9Y8cZJ"
                               "6vZl6YpKj1Z8JUWU")
    type: str = Field(description="Token Type", example="Bearer", default="Bearer")

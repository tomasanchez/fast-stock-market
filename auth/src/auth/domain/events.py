"""
Events that may occur in the application.

Events are notifications that are sent when something interesting happens in the system, such as an order being created,
 a user logging in, or a payment being processed.
"""
from pydantic import Field, UUID4

from auth.domain.models import ServiceStatus
from auth.domain.schemas import CamelCaseModel


class StatusChecked(CamelCaseModel):
    """
    The event is raised when the status of the actuator is checked.
    """

    name: str = Field(description="The name of the service.", example="redis")
    status: ServiceStatus = Field(description="The status of the service.", example=ServiceStatus.ONLINE)


class ReadinessChecked(CamelCaseModel):
    """
    The event is raised when the readiness of the actuator is checked.
    """
    status: ServiceStatus = Field(description="The status of the service.", example=ServiceStatus.ONLINE)
    services: list[StatusChecked] = Field(description="The list of services.",
                                          example=[StatusChecked(name="redis", status=ServiceStatus.ONLINE)],
                                          default_factory=list)


class UserCreated(CamelCaseModel):
    """
    Event raised when a user is created.
    """

    id: UUID4 = Field(description="The user id.", example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
    email: str = Field(description="The email.", example="john.doe@e.mail")

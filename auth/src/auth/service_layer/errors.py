"""
Service layer errors.
"""


class InvalidCredentialsError(Exception):
    """
    Exception raised when the username or passwords are invalid.
    """
    pass


class IllegalUserError(Exception):
    """
    Raised when a user wants to use a taken username or taken email.
    """
    pass

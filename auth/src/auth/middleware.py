from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_auth = HTTPBearer(scheme_name='JSON Web Token', description='Bearer JWT')

BearerTokenAuth = Annotated[HTTPAuthorizationCredentials, Depends(bearer_auth)]

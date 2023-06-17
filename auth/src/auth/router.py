"""Application configuration - root APIRouter.
Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications
"""
from fastapi import APIRouter

from auth.entrypoints import actuator
from auth.entrypoints.v1 import users, auth

root_router = APIRouter()
api_router_v1 = APIRouter(prefix="/api/v1")

# Base routers
root_router.include_router(actuator.router)

# API routers
api_router_v1.include_router(users.router)
api_router_v1.include_router(auth.router)

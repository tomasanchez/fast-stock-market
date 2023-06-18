"""
Users entrypoint
"""

from fastapi import APIRouter, Request, Response, status, HTTPException
from pydantic import UUID4

from auth.dependencies import UserRepositoryDependency, RegisterServiceDependency
from auth.domain.commands import RegisterUser
from auth.domain.events import UserCreated
from auth.domain.schemas import ResponseModels, ResponseModel

router = APIRouter(prefix="/users")


@router.get("/",
            status_code=status.HTTP_200_OK,
            tags=["Queries"])
async def query_users(user_repository: UserRepositoryDependency) -> ResponseModels[UserCreated]:
    """
    Retrieves a collection of users from the database.
    """

    users = await user_repository.find_all()

    return ResponseModels[UserCreated](data=[UserCreated(**user.dict()) for user in users])


@router.get("/{user_id}",
            status_code=status.HTTP_200_OK,
            tags=["Queries"])
async def query_user(user_id: UUID4,
                     user_repository: UserRepositoryDependency, ) -> ResponseModel[UserCreated]:
    """
    Retrieves a user from the database.
    """

    user = await user_repository.find_by({"_id": user_id})

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return ResponseModel[UserCreated](data=UserCreated(**user.dict()))


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             tags=["Commands"],
             )
async def create_user(command: RegisterUser,
                      register_service: RegisterServiceDependency,
                      request: Request,
                      response: Response,
                      ) -> ResponseModel[UserCreated]:
    """
    Allows to register a new user in the system.
    """

    try:
        user = await register_service.register(username=command.email, password=command.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    response.headers["Location"] = f"{request.base_url}api/v1/users/{user.id}"
    return ResponseModel[UserCreated](data=UserCreated(**user.dict()))

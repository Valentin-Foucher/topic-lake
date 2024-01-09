from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.dependencies import UsersRepositoryDependency, CreateUserPresenterDependency, \
    GetUserPresenterDependency
from topic_recommendations.api.models.users import CreateUserRequest, GetUserResponse, CreateUserResponse
from topic_recommendations.app.controllers.users.create import CreateUserController
from topic_recommendations.app.controllers.users.get import GetUserController

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, presenter: CreateUserPresenterDependency,
                      users_repository: UsersRepositoryDependency):
    return CreateUserController(presenter, users_repository).execute(
        user.name,
        user.password
    )


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=GetUserResponse)
async def get_user(user_id: int, presenter: GetUserPresenterDependency, users_repository: UsersRepositoryDependency):
    return GetUserController(presenter, users_repository).execute(user_id)

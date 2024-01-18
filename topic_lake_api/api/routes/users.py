from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from topic_lake_api.api.dependencies import UsersRepositoryDependency, CreateUserPresenterDependency, \
    GetUserPresenterDependency, AuthenticationDependency
from topic_lake_api.api.models.users import CreateUserRequest, GetUserResponse, CreateUserResponse
from topic_lake_api.app.controllers.users.create import CreateUserController
from topic_lake_api.app.controllers.users.get import GetUserController

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateUserResponse)
async def create_user(user: CreateUserRequest, presenter: CreateUserPresenterDependency,
                      users_repository: UsersRepositoryDependency):
    return CreateUserController(presenter, users_repository).execute(
        user.name,
        user.password
    )


@router.get('/self', status_code=status.HTTP_200_OK, response_model=GetUserResponse,
            dependencies=[AuthenticationDependency])
async def get_user(request: Request, presenter: GetUserPresenterDependency, users_repository: UsersRepositoryDependency):
    return GetUserController(presenter, users_repository).execute(request.user.id)

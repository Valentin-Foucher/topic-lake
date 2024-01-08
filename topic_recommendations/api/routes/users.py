from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.users import CreateUserRequest, GetUserResponse, CreateUserResponse
from topic_recommendations.app.controllers.users.create import CreateUserController
from topic_recommendations.app.controllers.users.get import GetUserController
from topic_recommendations.app.presenters.users import GetUserPresenter, CreateUserPresenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

UsersRepositoryDependency = \
    Annotated[IUsersRepository, Depends(partial(dependencies.get_repository, 'users'))]
GetUserPresenterDependency = \
    Annotated[GetUserPresenter, Depends(partial(dependencies.get_presenter, 'users', 'get'))]
CreateUserPresenterDependency = \
    Annotated[CreateUserPresenter, Depends(partial(dependencies.get_presenter, 'users', 'create'))]


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

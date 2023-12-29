from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.users import CreateUserModel
from topic_recommendations.app.controllers.users.create import CreateUserController
from topic_recommendations.app.controllers.users.get import GetUserController
from topic_recommendations.app.presenters.users import GetUserPresenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

UsersRepositoryDependency = \
    Annotated[IUsersRepository, Depends(partial(dependencies.get_repository, 'users'))]
GetUserPresenterDependency = \
    Annotated[GetUserPresenter, Depends(partial(dependencies.get_presenter, 'get'))]


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_users(user: CreateUserModel, users_repository: UsersRepositoryDependency):
    CreateUserController(users_repository).execute(
        user.name,
        user.password
    )


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_topic(user_id: int, presenter: GetUserPresenterDependency, users_repository: UsersRepositoryDependency):
    return GetUserController(presenter, users_repository).execute(user_id)

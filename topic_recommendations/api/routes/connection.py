from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.dependencies import UsersRepositoryDependency, AccessTokensRepositoryDependency, \
    LogInPresenterDependency
from topic_recommendations.api.models.connection import LogInRequest, LogOutRequest, LogInResponse
from topic_recommendations.app.controllers.connection.login import LogInController
from topic_recommendations.app.controllers.connection.logout import LogOutController

router = APIRouter(
    prefix='',
    tags=['connection']
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LogInResponse)
async def login(credentials: LogInRequest, presenter: LogInPresenterDependency,
                access_tokens_repository: AccessTokensRepositoryDependency,
                users_repository: UsersRepositoryDependency):
    return LogInController(presenter, access_tokens_repository, users_repository).execute(
        credentials.username,
        credentials.password
    )


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(logout_request: LogOutRequest, access_tokens_repository: AccessTokensRepositoryDependency,
                 users_repository: UsersRepositoryDependency):
    LogOutController(access_tokens_repository, users_repository).execute(logout_request.user_id)

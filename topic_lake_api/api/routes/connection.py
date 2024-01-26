from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from topic_lake_api.api.dependencies import UsersRepositoryDependency, AccessTokensRepositoryDependency, \
    LogInPresenterDependency, OptionalAuthenticationDependency, DBDependency
from topic_lake_api.api.models.connection import LogInRequest, LogInResponse
from topic_lake_api.app.controllers.connection.login import LogInController
from topic_lake_api.app.controllers.connection.logout import LogOutController

router = APIRouter(
    prefix='',
    tags=['connection']
)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LogInResponse)
async def login(db: DBDependency, credentials: LogInRequest, presenter: LogInPresenterDependency,
                access_tokens_repository: AccessTokensRepositoryDependency,
                users_repository: UsersRepositoryDependency):
    return await LogInController(presenter, access_tokens_repository, users_repository).execute(
        credentials.username,
        credentials.password
    )


@router.post('/logout', status_code=status.HTTP_200_OK, dependencies=[OptionalAuthenticationDependency])
async def logout(db: DBDependency, request: Request, access_tokens_repository: AccessTokensRepositoryDependency,
                 users_repository: UsersRepositoryDependency):
    await LogOutController(access_tokens_repository, users_repository).execute(
        request.user.id if request.user else None
    )

from functools import wraps

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from topic_lake_api.api.exceptions import Unauthorized, NotFound
from topic_lake_api.infra.db.core import sessionmanager
from topic_lake_api.infra.repositories.access_tokens import AccessTokensRepository
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.infra.repositories.users import UsersRepository
from topic_lake_api.utils.crypto_utils import decode_jwt


async def ensure_authentication(request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    user_id = decode_jwt(token)

    if not user_id:
        raise Unauthorized('Unauthorized')

    async with sessionmanager.session() as db:
        access_tokens_repository = AccessTokensRepository().with_session(db)
        match await access_tokens_repository.is_revoked(token):
            case None:
                raise Unauthorized('Invalid token')
            case True:
                await access_tokens_repository.create(user_id)

        users_repository = UsersRepository().with_session(db)
        user = await users_repository.get(user_id)
        if not user:
            raise NotFound(f'User {user_id} not found')

        request.scope['user'] = user


async def ensure_authentication_if_authenticated(
        request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    request.scope['user'] = None
    if not credentials:
        return

    token = credentials.credentials
    user_id = decode_jwt(token)

    if not user_id:
        return

    async with sessionmanager.session() as db:
        user = await UsersRepository().with_session(db).get(user_id)
        if not user:
            raise NotFound(f'User {user_id} not found')

        request.scope['user'] = user


def with_repositories(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        if 'db' in kwargs:
            for parameter in kwargs.values():
                if isinstance(parameter, SQLRepository):
                    parameter.with_session(kwargs['db'])
            return await f(*args, **kwargs)

    return wrapper

from functools import wraps

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from topic_lake_api.api.exceptions import Unauthorized, NotFound
from topic_lake_api.domain.utils.jwt_utils import decode_jwt
from topic_lake_api.infra.db.core import get_session
from topic_lake_api.infra.repositories.access_tokens import AccessTokensRepository
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.infra.repositories.users import UsersRepository


async def ensure_authentication(request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    user_id = decode_jwt(token)

    if not user_id:
        raise Unauthorized('Unauthorized')

    with get_session() as session:
        access_tokens_repository = AccessTokensRepository().with_session(session)
        match access_tokens_repository.is_revoked(token):
            case None:
                raise Unauthorized('Invalid token')
            case True:
                access_tokens_repository.create(user_id)

        user = UsersRepository().with_session(session).get(user_id)
        if not user:
            raise NotFound(f'User {user_id} not found')

        request.scope['user'] = user


async def ensure_authentication_if_authenticated(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    request.scope['user'] = None
    if not credentials:
        return

    token = credentials.credentials
    user_id = decode_jwt(token)

    if not user_id:
        return

    with get_session() as session:
        user = UsersRepository().with_session(session).get(user_id)
        if not user:
            raise NotFound(f'User {user_id} not found')

        request.scope['user'] = user


def inject_scoped_session_in_repositories(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        with get_session() as session:
            for parameter in kwargs.values():
                if isinstance(parameter, SQLRepository):
                    parameter.with_session(session)
            return await f(*args, **kwargs)

    return wrapper

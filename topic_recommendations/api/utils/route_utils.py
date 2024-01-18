from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from topic_recommendations.api.exceptions import Unauthorized, NotFound
from topic_recommendations.infra.repositories.access_tokens import AccessTokensRepository
from topic_recommendations.infra.repositories.users import UsersRepository
from topic_recommendations.utils.crypto_utils import decode_jwt


async def ensure_authentication(request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    user_id = decode_jwt(token)

    if not user_id:
        raise Unauthorized('Unauthorized')

    access_tokens_repository = AccessTokensRepository()
    match access_tokens_repository.is_revoked(token):
        case None:
            raise Unauthorized('Invalid token')
        case True:
            access_tokens_repository.create(user_id)

    user = UsersRepository().get(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')

    request.scope['user'] = user

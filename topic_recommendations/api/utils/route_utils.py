from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from topic_recommendations.api.exceptions import Unauthorized, NotFound
from topic_recommendations.infra.repositories.access_tokens import AccessTokensRepository
from topic_recommendations.infra.repositories.users import UsersRepository


async def ensure_authentication(request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    access_tokens_repository = AccessTokensRepository()
    user_id, revoked = access_tokens_repository.get_user_id_for_value(credentials.credentials)

    if not user_id:
        raise Unauthorized('Unauthorized')

    user = UsersRepository().get(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')

    if revoked:
        access_tokens_repository.create(user_id)

    request.scope['user'] = user

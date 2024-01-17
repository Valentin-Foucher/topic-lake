from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from topic_recommendations.api.exceptions import Unauthorized, NotFound
from topic_recommendations.infra.repositories.access_tokens import AccessTokensRepository
from topic_recommendations.infra.repositories.users import UsersRepository


async def ensure_authentication(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = AccessTokensRepository().get_user_id_for_value(credentials.credentials)
    if not user_id:
        raise Unauthorized('Unauthorized')

    user = UsersRepository().get(user_id)
    if not user:
        raise NotFound(f'User {user_id} not found')

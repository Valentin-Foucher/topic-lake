from datetime import datetime
from typing import Optional

import jwt
from jwt import DecodeError

from topic_lake_api import config
from topic_lake_api.constants import TOKEN_MAX_DURATION


def encode_jwt(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'expires': datetime.utcnow().timestamp() + TOKEN_MAX_DURATION
    }
    return jwt.encode(payload, config.get('jwt.secret_key'), algorithm=config.get('jwt.algorithm'))


def decode_jwt(token: str) -> Optional[int]:
    try:
        decoded_token = jwt.decode(token, config.get('jwt.secret_key'), algorithms=[config.get('jwt.algorithm')])
    except DecodeError:
        return
    if decoded_token.get('expires', 0) < datetime.utcnow().timestamp():
        return
    return decoded_token.get('user_id')

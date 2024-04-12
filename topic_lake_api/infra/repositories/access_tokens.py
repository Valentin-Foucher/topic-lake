from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, and_, update
from sqlalchemy.exc import NoResultFound

from topic_lake_api.constants import TOKEN_MAX_DURATION
from topic_lake_api.domain.interfaces.repositories import IAccessTokensRepository
from topic_lake_api.domain.utils.crypto_utils import encode_jwt
from topic_lake_api.infra.db.models import AccessToken
from topic_lake_api.infra.repositories.base import SQLRepository


class AccessTokensRepository(SQLRepository, IAccessTokensRepository):
    def _get_by_id(self, token_id: int):
        try:
            return self._session.scalars(
                select(AccessToken)
                .where(AccessToken.id == token_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

    def create(self, user_id: int) -> str:
        token_value = encode_jwt(user_id)
        t = AccessToken(value=token_value, user_id=user_id)

        self._session.add(t)
        self._session.flush()

        return token_value

    def get_latest(self, user_id: int) -> Optional[str]:
        try:
            t = self._session.scalars(
                select(AccessToken)
                .where(
                    and_(
                        AccessToken.user_id == user_id,
                        AccessToken.revoked.is_(False),
                        AccessToken.creation_date > datetime.utcnow() - timedelta(seconds=TOKEN_MAX_DURATION))
                )
                .order_by(AccessToken.creation_date.desc())
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return t.value

    def delete_all(self, user_id: int):
        self._session.execute(
            update(AccessToken)
            .where(
                and_(
                    AccessToken.user_id == user_id,
                    AccessToken.revoked.is_(False)
                )
            )
            .values(revoked=True)
        )

    def is_revoked(self, value: str) -> Optional[bool]:
        try:
            t = self._session.scalars(
                select(AccessToken)
                .where(AccessToken.value == value)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return t.revoked

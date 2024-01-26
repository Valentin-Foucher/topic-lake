from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, and_, update
from sqlalchemy.exc import NoResultFound

from topic_lake_api.constants import TOKEN_MAX_DURATION
from topic_lake_api.infra.db.models import AccessToken
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_lake_api.utils.crypto_utils import encode_jwt


class AccessTokensRepository(SQLRepository, IAccessTokensRepository):

    async def _get_by_id(self, token_id: int):
        try:
            return (await self._db.scalars(
                select(AccessToken)
                .where(AccessToken.id == token_id)
                .limit(1)
            )).one()
        except NoResultFound:
            return None

    async def create(self, user_id: int) -> str:
        token_value = encode_jwt(user_id)
        t = AccessToken(value=token_value, user_id=user_id)
        self._db.add(t)
        await self._db.commit()
        await self._db.flush()

        return token_value

    async def get_latest(self, user_id: int) -> Optional[str]:
        try:
            t = (await self._db.scalars(
                select(AccessToken)
                .where(
                    and_(
                        AccessToken.user_id == user_id,
                        AccessToken.revoked.is_(False),
                        AccessToken.creation_date > datetime.utcnow() - timedelta(seconds=TOKEN_MAX_DURATION))
                )
                .order_by(AccessToken.creation_date.desc())
                .limit(1)
            )).one()
        except NoResultFound:
            return None

        return t.value

    async def delete_all(self, user_id: int):
        await self._db.execute(
            update(AccessToken)
            .where(
                and_(
                    AccessToken.user_id == user_id,
                    AccessToken.revoked.is_(False)
                )
            )
            .values(revoked=True)
        )
        await self._db.commit()

    async def is_revoked(self, value: str) -> Optional[bool]:
        try:
            t = (await self._db.scalars(
                select(AccessToken)
                .where(AccessToken.value == value)
                .limit(1)
            )).one()
        except NoResultFound:
            return None

        return t.revoked

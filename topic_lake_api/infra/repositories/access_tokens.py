from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, and_, update
from sqlalchemy.exc import NoResultFound

from topic_lake_api.constants import TOKEN_MAX_DURATION
from topic_lake_api.infra.db.core import session
from topic_lake_api.infra.db.models import AccessToken
from topic_lake_api.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_lake_api.utils.crypto_utils import encode_jwt


class AccessTokensRepository(IAccessTokensRepository):
    @staticmethod
    def _get_by_id(token_id: int):
        try:
            return session.scalars(
                select(AccessToken)
                .where(AccessToken.id == token_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

    def create(self, user_id: int) -> str:
        token_value = encode_jwt(user_id)
        t = AccessToken(value=token_value, user_id=user_id)
        try:
            session.add(t)
        except:
            session.rollback()
            raise
        else:
            session.flush()
            session.commit()

        return token_value

    def get_latest(self, user_id: int) -> Optional[str]:
        try:
            t = session.scalars(
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
        session.execute(
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
            t = session.scalars(
                select(AccessToken)
                .where(AccessToken.value == value)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

        return t.revoked

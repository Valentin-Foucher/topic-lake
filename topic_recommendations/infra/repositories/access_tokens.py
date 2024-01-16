from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import AccessToken
from topic_recommendations.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository


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

    def create(self, value: str, user_id: int):
        t = AccessToken(value=value, user_id=user_id)
        session.add(t)
        session.commit()

    def get_latest(self, user_id: int) -> Optional[str]:
        try:
            return session.scalars(
                select(AccessToken)
                .where(AccessToken.user_id == user_id)
                .order_by(AccessToken.creation_date.desc())
                .limit(1)
            ).one()
        except NoResultFound:
            return None

    def delete(self, token_id: int) -> bool:
        try:
            token = session.scalars(
                select(AccessToken)
                .where(AccessToken.id == token_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return False

        session.delete(token)
        session.commit()
        return True

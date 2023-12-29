from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_recommendations.domain.entities.users import User
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import User as UserModel
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository


class UsersRepository(IUsersRepository):
    def create(self, name: str, hashed_password: str):
        session.add(UserModel(name=name, password=hashed_password))
        session.commit()

    def get(self, user_id: int) -> Optional[User]:
        try:
            user = session.scalars(
                select(UserModel).filter_by(id=user_id).limit(1)
            ).one()
        except NoResultFound:
            return None

        return User(**user.mappings().all())

    def get_by_name(self, name: str) -> Optional[User]:
        try:
            user = session.scalars(
                select(UserModel).filter_by(name=name).limit(1)
            ).one()
        except NoResultFound:
            return None

        return User(**user.mappings().all())

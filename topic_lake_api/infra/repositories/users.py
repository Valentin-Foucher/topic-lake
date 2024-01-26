from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_lake_api.domain.entities.users import User
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository


class UsersRepository(SQLRepository, IUsersRepository):
    async def create(self, name: str, hashed_password: str) -> int:
        u = UserModel(name=name, password=hashed_password)

        self._db.add(u)
        await self._db.commit()
        await self._db.flush()

        return u.id

    async def get(self, user_id: int) -> Optional[User]:
        try:
            user = (await self._db.scalars(
                select(UserModel)
                .where(UserModel.id == user_id)
                .limit(1)
            )).one()
        except NoResultFound:
            return None

        return user.as_dataclass()

    async def get_by_name(self, name: str) -> Optional[User]:
        try:
            user = (await self._db.scalars(
                select(UserModel)
                .where(UserModel.name == name)
                .limit(1)
            )).one()
        except NoResultFound:
            return None

        return user.as_dataclass()

import dataclasses

from topic_lake_api.domain.entities.users import User
from topic_lake_api.interactor.interfaces.base import Presenter


class GetUserPresenter(Presenter):
    def present(self, user: User):
        return {'user': dataclasses.asdict(user)}


class CreateUserPresenter(Presenter):
    def present(self, inserted_id: int):
        return {'id': inserted_id}

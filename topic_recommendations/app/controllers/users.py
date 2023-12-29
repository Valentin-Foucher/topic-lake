from fastapi import HTTPException
from starlette import status

from topic_recommendations.app.presenters.users import GetUserPresenter
from topic_recommendations.app.controllers.base import Controller
from topic_recommendations.exceptions import BadRequest, NotFound
from topic_recommendations.interactor.exceptions import AlreadyExist
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.users.create_user import CreateUser
from topic_recommendations.interactor.use_cases.users.get_user import GetUser


class UsersController(Controller):
    _repository: IUsersRepository

    def create(self, name: str, password: str):
        try:
            CreateUser(self._repository).execute(name, password)
        except AlreadyExist:
            raise BadRequest("User already exists")

    def get(self, topic_id: int):
        result = GetUser(GetUserPresenter(), self._repository).execute(topic_id)
        if not result:
            raise NotFound("User not found")
        return result

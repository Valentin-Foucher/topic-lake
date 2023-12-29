from fastapi import HTTPException
from starlette import status

from topic_recommendations.app.presenters.users import GetUserPresenter
from topic_recommendations.app.views.base import Controller
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    def get(self, topic_id: int):
        result = GetUser(GetUserPresenter(), self._repository).execute(topic_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return result

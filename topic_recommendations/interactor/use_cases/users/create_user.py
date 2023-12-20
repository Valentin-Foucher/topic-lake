from topic_recommendations.interactor.exceptions import AlreadyExist
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateUser(UseCase):
    def __init__(self, repository: IUsersRepository):
        self._repository = repository

    def execute(self, name: str, password: str):
        if self._repository.get_by_name(name):
            raise AlreadyExist

        # TODO -> hash password
        hashed_password = password

        self._repository.create(name, hashed_password)

from topic_recommendations.interactor.exceptions import AlreadyExist
from topic_recommendations.interactor.interfaces.base import Presenter
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository
from topic_recommendations.interactor.use_cases.base import UseCase


class CreateUser(UseCase):
    def __init__(self, presenter: Presenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    def execute(self, name: str, password: str):
        if self._repository.get_by_name(name):
            raise AlreadyExist(f'User "{name}" already exists')

        # TODO -> hash password
        hashed_password = password

        inserted_id = self._repository.create(name, hashed_password)
        return self._presenter.present(inserted_id)

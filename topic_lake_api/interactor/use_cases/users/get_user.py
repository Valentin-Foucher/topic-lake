from topic_lake_api.interactor.exceptions import DoesNotExist
from topic_lake_api.interactor.interfaces.base import Presenter
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.base import UseCase


class GetUser(UseCase):
    def __init__(self, presenter: Presenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    async def execute(self, user_id: int):
        result = await self._repository.get(user_id)
        if not result:
            raise DoesNotExist(f'User {user_id} does not exist')
        return self._presenter.present(result)

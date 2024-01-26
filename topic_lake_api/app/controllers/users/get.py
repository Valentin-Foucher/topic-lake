from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.app.presenters.users import GetUserPresenter
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.users.get_user import GetUser


class GetUserController(Controller):
    def __init__(self, presenter: GetUserPresenter, repository: IUsersRepository):
        self._presenter = presenter
        self._repository = repository

    async def execute(self, user_id: int):
        return await GetUser(self._presenter, self._repository).execute(user_id)


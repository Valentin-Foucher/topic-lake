from topic_lake_api.app.controllers.base import Controller
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository
from topic_lake_api.interactor.use_cases.topics.delete_topic import DeleteTopic


class DeleteTopicController(Controller):
    def __init__(self, topics_repository: ITopicsRepository, users_repository: IUsersRepository):
        self._topics_repository = topics_repository
        self._users_repository = users_repository

    async def execute(self, user_id: int, topic_id: int):
        await DeleteTopic(self._topics_repository, self._users_repository).execute(
            user_id,
            topic_id
        )

import dataclasses

from topic_lake_api.domain.entities.topics import Topic
from topic_lake_api.interactor.interfaces.base import Presenter


class ListTopicsPresenter(Presenter):
    def present(self, topics_list: list[Topic]):
        return {'topics': [dataclasses.asdict(topic) for topic in topics_list]}


class GetTopicPresenter(Presenter):
    def present(self, topic: Topic):
        return {'topic': dataclasses.asdict(topic)}


class CreateTopicPresenter(Presenter):
    def present(self, inserted_id: int):
        return {'id': inserted_id}


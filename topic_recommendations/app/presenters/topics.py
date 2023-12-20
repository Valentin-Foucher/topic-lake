import dataclasses

from topic_recommendations.app.presenters.base import Presenter
from topic_recommendations.interactor.dtos.outputs.topics import GetTopicOutputDto, ListTopicsOutputDto


class ListTopicsPresenter(Presenter):
    def present(self, output_dto: ListTopicsOutputDto):
        return {'topics': [dataclasses.asdict(topic) for topic in output_dto.topic_list]}


class GetTopicPresenter(Presenter):
    def present(self, output_dto: GetTopicOutputDto):
        return {'topic': dataclasses.asdict(output_dto.topic)}

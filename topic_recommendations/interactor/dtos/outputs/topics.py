from dataclasses import dataclass

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.interactor.dtos.outputs.base import OutputDto


@dataclass
class ListTopicsOutputDto(OutputDto):
    topic_list: list[Topic]


@dataclass
class GetTopicOutputDto(OutputDto):
    topic: Topic

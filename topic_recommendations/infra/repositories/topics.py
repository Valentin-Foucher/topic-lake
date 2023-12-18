from sqlalchemy import select

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Topic as TopicModel
from topic_recommendations.interactor.dtos.outputs.topics import ListTopicsOutputDto, GetTopicOutputDto
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(ITopicsRepository):
    def list(self, limit: int = 100) -> ListTopicsOutputDto:
        topic_list = session.scalars(
            select(TopicModel).limit(limit)
        ).all()
        return ListTopicsOutputDto(topic_list=[Topic(**topic.as_dict()) for topic in topic_list])

    def create(self, user_id: int, content: str):
        session.add(TopicModel(user_id=user_id, content=content))
        session.commit()

    def get(self, topic_id: int) -> GetTopicOutputDto:
        topic = session.scalars(
            select(TopicModel).filter_by(id=topic_id).limit(1)
        ).one()
        return GetTopicOutputDto(topic=Topic(**topic.as_dict()))

    def delete(self, topic_id: int):
        topic = self.get(topic_id)
        session.delete(topic)
        session.commit()

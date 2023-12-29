from sqlalchemy import select

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Topic as TopicModel
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(ITopicsRepository):
    @staticmethod
    def _get_by_id(topic_id: int):
        return session.scalars(
            select(TopicModel).filter_by(id=topic_id).limit(1)
        ).one()

    def list(self, limit: int = 100) -> list[Topic]:
        topic_list = session.scalars(
            select(TopicModel).limit(limit)
        ).all()
        return [topic.as_dataclass(Topic) for topic in topic_list]

    def create(self, user_id: int, content: str):
        session.add(TopicModel(user_id=user_id, content=content))
        session.commit()

    def get(self, topic_id: int) -> Topic:
        topic = self._get_by_id(topic_id)
        return topic.as_dataclass(Topic)

    def delete(self, topic_id: int):
        topic = self._get_by_id(topic_id)
        session.delete(topic)
        session.commit()

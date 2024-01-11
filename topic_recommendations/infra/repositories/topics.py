from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from topic_recommendations.domain.entities.topics import Topic
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Topic as TopicModel
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(ITopicsRepository):
    @staticmethod
    def _get_by_id(topic_id: int):
        try:
            return session.scalars(
                select(TopicModel)
                .where(TopicModel.id == topic_id)
                .limit(1)
            ).one()
        except NoResultFound:
            return None

    def list(self, limit: int = 100) -> list[Topic]:
        topic_list = session.scalars(
            select(TopicModel)
            .limit(limit)
        ).all()

        return [topic.as_dataclass(Topic) for topic in topic_list]

    def create(self, user_id: int, parent_topic_id: Optional[int], content: str) -> int:
        t = TopicModel(user_id=user_id, parent_topic_id=parent_topic_id, content=content)
        session.add(t)
        session.flush()
        session.commit()
        return t.id

    def get(self, topic_id: int) -> Topic:
        topic = self._get_by_id(topic_id)
        return topic.as_dataclass(Topic) if topic else None

    def delete(self, topic_id: int) -> bool:
        topic = self._get_by_id(topic_id)
        if not topic:
            return False

        session.delete(topic)
        session.commit()
        return True

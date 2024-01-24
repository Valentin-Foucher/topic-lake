from typing import Optional

from sqlalchemy import select, null, literal, and_, or_, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased

from topic_lake_api.domain.entities.topics import Topic
from topic_lake_api.infra.db.core import session
from topic_lake_api.infra.db.models import Topic as TopicModel
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(ITopicsRepository):

    @staticmethod
    def _get_topics_as_treeview(*filters: list[bool], limit: int = 1):
        anchor_member = session.query(TopicModel, literal(0).label('level')) \
            .filter(*filters) \
            .order_by(TopicModel.id) \
            .limit(limit) \
            .cte(name='ancestors_id', recursive=True)

        parent = aliased(anchor_member, name='p')
        children = aliased(TopicModel, name='c')

        recursive_member = anchor_member.union_all(
            session
            .query(children, (parent.c.level + 1).label('level'))
            .filter(children.parent_topic_id == parent.c.id)
            .order_by(parent.c.id)
        )

        return session.scalars(
            select(TopicModel, recursive_member.c.level)
            .where(
                and_(
                    TopicModel.id == recursive_member.c.id,
                    recursive_member.c.level == 0
                )
            )
        )

    def list(self, limit: int = 100) -> list[Topic]:
        topic_list = self._get_topics_as_treeview(TopicModel.parent_topic == null(), limit=limit)
        return [topic.as_dataclass() for topic in topic_list]

    def create(self, user_id: int, parent_topic_id: Optional[int], content: str) -> int:
        t = TopicModel(user_id=user_id, parent_topic_id=parent_topic_id, content=content)
        try:
            session.add(t)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()
        return t.id

    def get(self, topic_id: int) -> Optional[Topic]:
        try:
            topic = self._get_topics_as_treeview(TopicModel.id == topic_id) \
                .one()
        except NoResultFound:
            return None

        return topic.as_dataclass()

    def delete(self, user_id: int, topic_id: int) -> bool:
        deleted_rows = \
            session.execute(
                delete(TopicModel).filter(
                    and_(
                        UserModel.id == user_id,
                        or_(
                            UserModel.admin.is_(True),
                            and_(
                                TopicModel.id == topic_id,
                                TopicModel.user_id == user_id
                            )
                        )
                    )
                ).returning(TopicModel.id)
            ).fetchall()

        return len(deleted_rows) != 0

    def update(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        session.execute(
            update(TopicModel).filter(
                and_(
                    TopicModel.user_id == user_id,
                    TopicModel.id == topic_id
                    )
            ).values(content=content, parent_topic_id=parent_topic_id)
        )

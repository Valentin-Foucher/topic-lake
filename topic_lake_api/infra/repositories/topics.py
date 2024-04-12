from typing import Optional

from sqlalchemy import select, null, literal, and_, or_, delete, update, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased

from topic_lake_api.domain.entities.topics import Topic
from topic_lake_api.domain.interfaces.repositories import ITopicsRepository
from topic_lake_api.infra.db.models import Topic as TopicModel
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository


class TopicsRepository(SQLRepository, ITopicsRepository):

    def _get_topics_as_treeview(self, *filters: list[bool], limit: int = 1):
        anchor_member = self._session.query(TopicModel, literal(0).label('level')) \
            .filter(*filters) \
            .limit(limit) \
            .cte(name='ancestors_id', recursive=True)

        parent = aliased(anchor_member, name='p')
        children = aliased(TopicModel, name='c')

        recursive_member = anchor_member.union_all(
            self._session
            .query(children, (parent.c.level + 1).label('level'))
            .filter(children.parent_topic_id == parent.c.id)
            .order_by(parent.c.content)
        )

        return self._session.scalars(
            select(TopicModel, recursive_member.c.level)
            .where(
                and_(
                    TopicModel.id == recursive_member.c.id,
                    recursive_member.c.level == 0
                )
            ).order_by(TopicModel.content)
        )

    def list(self, limit: int = 1000) -> list[Topic]:
        topic_list = self._get_topics_as_treeview(TopicModel.parent_topic == null(), limit=limit)
        return [topic.as_dataclass() for topic in topic_list]

    def create(self, user_id: int, parent_topic_id: Optional[int], content: str) -> int:
        t = TopicModel(user_id=user_id, parent_topic_id=parent_topic_id, content=content)

        self._session.add(t)
        self._session.flush()

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
            self._session.execute(
                delete(TopicModel).filter(
                    and_(
                        TopicModel.id == topic_id,
                        or_(
                            UserModel.admin.is_(True),
                            TopicModel.user_id == user_id
                        )
                    )
                ).returning(TopicModel.id)
            ).fetchall()

        result = len(deleted_rows) != 0
        return result

    def update(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        self._session.execute(
            update(TopicModel).filter(
                and_(
                    TopicModel.id == topic_id,
                    or_(
                        UserModel.admin.is_(True),
                        TopicModel.user_id == user_id
                    )
                )
            ).values(content=content, parent_topic_id=parent_topic_id)
        )

    def exists(self, parent_topic_id: Optional[int], content: str) -> bool:
        try:
            self._session.scalars(
                select(TopicModel)
                .where(
                    and_(
                        TopicModel.parent_topic_id == parent_topic_id,
                        func.lower(TopicModel.content) == content.lower(),
                    )
                ).limit(1)
            ).one()
        except NoResultFound:
            return False

        return True

from typing import Optional

from sqlalchemy import select, null, literal, and_, or_, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased

from topic_lake_api.domain.entities.topics import Topic
from topic_lake_api.infra.db.models import Topic as TopicModel
from topic_lake_api.infra.db.models import User as UserModel
from topic_lake_api.infra.repositories.base import SQLRepository
from topic_lake_api.infra.utils.sqlalchemy_utils import with_join_depth
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository


class TopicsRepository(SQLRepository, ITopicsRepository):
    MAX_DEPTH = 10

    async def _get_topics_as_treeview(self, *filters: list[bool], limit: int = 1):
        anchor_member = \
            select(TopicModel, literal(0).label('level')) \
            .where(and_(*filters)) \
            .limit(limit) \
            .cte(name='ancestors_id', recursive=True)

        parent = aliased(anchor_member, name='p')
        children = aliased(TopicModel, name='c')

        recursive_member = anchor_member.union_all(
            select(children, (parent.c.level + 1).label('level'))
            .where(
                and_(
                    children.parent_topic_id == parent.c.id,
                    parent.c.level <= self.MAX_DEPTH
                )
            ).order_by(parent.c.id)
        )

        return (await self._db.scalars(
            select(TopicModel, recursive_member.c.level)
            .where(
                and_(
                    TopicModel.id == recursive_member.c.id,
                    recursive_member.c.level == 0
                )
            )
            .order_by(TopicModel.id)
        )).unique()

    @with_join_depth(TopicModel.sub_topics, MAX_DEPTH)
    async def list(self, limit: int = 100) -> list[Topic]:
        topic_list = await self._get_topics_as_treeview(TopicModel.parent_topic == null(), limit=limit)
        return [topic.as_dataclass(with_sub_children=True) for topic in topic_list]

    async def create(self, user_id: int, parent_topic_id: Optional[int], content: str) -> int:
        t = TopicModel(user_id=user_id, parent_topic_id=parent_topic_id, content=content)

        self._db.add(t)
        await self._db.commit()
        await self._db.flush()

        return t.id

    async def get(self, topic_id: int) -> Optional[Topic]:
        try:
            topic = (await self._get_topics_as_treeview(TopicModel.id == topic_id)) \
                .one()
        except NoResultFound:
            return None

        return topic.as_dataclass()

    async def delete(self, user_id: int, topic_id: int) -> bool:
        deleted_rows = \
            (await self._db.execute(
                delete(TopicModel).filter(
                    and_(
                        TopicModel.id == topic_id,
                        or_(
                            UserModel.admin.is_(True),
                            TopicModel.user_id == user_id
                        )
                    )
                ).returning(TopicModel.id)
            )).fetchall()

        result = len(deleted_rows) != 0
        await self._db.commit()
        return result

    async def update(self, user_id: int, topic_id: int, parent_topic_id: Optional[int], content: str):
        await self._db.execute(
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
        await self._db.commit()

    async def exists(self, parent_topic_id: Optional[int], content: str) -> bool:
        try:
            (await self._db.scalars(
                select(TopicModel)
                .where(
                    and_(
                        TopicModel.parent_topic_id == parent_topic_id,
                        TopicModel.content == content,
                    )
                ).limit(1)
            )).unique().one()
        except NoResultFound:
            return False

        return True

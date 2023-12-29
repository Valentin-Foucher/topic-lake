from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.models.topics import CreateTopicModel
from topic_recommendations.app.controllers.topics import TopicsUsers
from topic_recommendations.infra.repositories.topics import TopicsRepository

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)
view = TopicsUsers(TopicsRepository())


@router.get('', status_code=status.HTTP_200_OK)
async def list_topics():
    return view.list()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_topic(topic: CreateTopicModel):
    view.create(topic.user_id, topic.content)


@router.get('/{topic_id}', status_code=status.HTTP_200_OK)
async def get_topic(topic_id: int):
    return view.get(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int):
    view.delete(topic_id)

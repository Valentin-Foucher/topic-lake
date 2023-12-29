from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.models.topics import CreateTopicModel
from topic_recommendations.app.controllers.topics import TopicsController
from topic_recommendations.infra.repositories.topics import TopicsRepository

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)


@router.get('', status_code=status.HTTP_200_OK)
async def listtopics():
    return TopicsController() \
        .with_repository(TopicsRepository()) \
        .list()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_topic(topic: CreateTopicModel):
    TopicsController() \
        .with_repository(TopicsRepository()) \
        .create(
            topic.user_id,
            topic.content
        )


@router.get('/{topic_id}', status_code=status.HTTP_200_OK)
async def get_topic(topic_id: int):
    return TopicsController() \
        .with_repository(TopicsRepository()) \
        .get(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int):
    TopicsController() \
        .with_repository(TopicsRepository()) \
        .delete(topic_id)

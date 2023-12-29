from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.topics import CreateTopicModel
from topic_recommendations.app.controllers.topics import TopicsController
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

TopicsRepositoryDependency = \
    Annotated[ITopicsRepository, Depends(partial(dependencies.get_repository, 'topics'))]


@router.get('', status_code=status.HTTP_200_OK)
async def list_topics(topics_repository: TopicsRepositoryDependency):
    return TopicsController() \
        .with_repository(topics_repository) \
        .list()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_topic(topic: CreateTopicModel, topics_repository: TopicsRepositoryDependency):
    TopicsController() \
        .with_repository(topics_repository) \
        .create(
            topic.user_id,
            topic.content
        )


@router.get('/{topic_id}', status_code=status.HTTP_200_OK)
async def get_topic(topic_id: int, topics_repository: TopicsRepositoryDependency):
    return TopicsController() \
        .with_repository(topics_repository) \
        .get(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int, topics_repository: TopicsRepositoryDependency):
    TopicsController() \
        .with_repository(topics_repository) \
        .delete(topic_id)

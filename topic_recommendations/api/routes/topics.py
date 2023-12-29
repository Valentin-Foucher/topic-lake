from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.topics import CreateTopicRequest, GetTopicResponse, ListTopicsResponse
from topic_recommendations.app.controllers.topics.create import CreateTopicController
from topic_recommendations.app.controllers.topics.delete import DeleteTopicController
from topic_recommendations.app.controllers.topics.get import GetTopicController
from topic_recommendations.app.controllers.topics.list import ListTopicsController
from topic_recommendations.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository

router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

TopicsRepositoryDependency = \
    Annotated[ITopicsRepository, Depends(partial(dependencies.get_repository, 'topics'))]
ListTopicsPresenterDependency = \
    Annotated[ListTopicsPresenter, Depends(partial(dependencies.get_presenter, 'list'))]
GetTopicPresenterDependency = \
    Annotated[GetTopicPresenter, Depends(partial(dependencies.get_presenter, 'get'))]


@router.get('', status_code=status.HTTP_200_OK, response_model=ListTopicsResponse)
async def list_topics(presenter: ListTopicsPresenterDependency, topics_repository: TopicsRepositoryDependency):
    return ListTopicsController(presenter, topics_repository).execute()


@router.post('', status_code=status.HTTP_204_NO_CONTENT)
async def create_topic(topic: CreateTopicRequest, topics_repository: TopicsRepositoryDependency):
    CreateTopicController(topics_repository).execute(
        topic.user_id,
        topic.content
    )


@router.get('/{topic_id}', status_code=status.HTTP_200_OK, response_model=GetTopicResponse)
async def get_topic(topic_id: int, presenter: GetTopicPresenterDependency,
                    topics_repository: TopicsRepositoryDependency):
    return GetTopicController(presenter, topics_repository).execute(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int, topics_repository: TopicsRepositoryDependency):
    DeleteTopicController(topics_repository).execute(topic_id)

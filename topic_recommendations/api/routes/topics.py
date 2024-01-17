from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.dependencies import ListTopicsPresenterDependency, TopicsRepositoryDependency, \
    GetTopicPresenterDependency, UsersRepositoryDependency, CreateTopicPresenterDependency, AuthenticationDependency
from topic_recommendations.api.models.topics import CreateTopicRequest, GetTopicResponse, ListTopicsResponse, \
    CreateTopicResponse
from topic_recommendations.app.controllers.topics.create import CreateTopicController
from topic_recommendations.app.controllers.topics.delete import DeleteTopicController
from topic_recommendations.app.controllers.topics.get import GetTopicController
from topic_recommendations.app.controllers.topics.list import ListTopicsController

router = APIRouter(
    prefix='/topics',
    tags=['topics'],
    dependencies=[AuthenticationDependency]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=ListTopicsResponse)
async def list_topics(presenter: ListTopicsPresenterDependency, topics_repository: TopicsRepositoryDependency):
    return ListTopicsController(presenter, topics_repository).execute()


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateTopicResponse)
async def create_topic(topic: CreateTopicRequest, presenter: CreateTopicPresenterDependency,
                       topics_repository: TopicsRepositoryDependency,
                       users_repository: UsersRepositoryDependency):
    return CreateTopicController(presenter, topics_repository, users_repository).execute(
        topic.user_id,
        topic.parent_topic_id,
        topic.content
    )


@router.get('/{topic_id}', status_code=status.HTTP_200_OK, response_model=GetTopicResponse)
async def get_topic(topic_id: int, presenter: GetTopicPresenterDependency,
                    topics_repository: TopicsRepositoryDependency):
    return GetTopicController(presenter, topics_repository).execute(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(topic_id: int, topics_repository: TopicsRepositoryDependency):
    DeleteTopicController(topics_repository).execute(topic_id)

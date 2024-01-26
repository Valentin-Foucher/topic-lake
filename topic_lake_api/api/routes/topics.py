from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from topic_lake_api.api.dependencies import ListTopicsPresenterDependency, TopicsRepositoryDependency, \
    GetTopicPresenterDependency, UsersRepositoryDependency, CreateTopicPresenterDependency, AuthenticationDependency, \
    DBDependency
from topic_lake_api.api.models.topics import CreateTopicRequest, GetTopicResponse, ListTopicsResponse, \
    CreateTopicResponse, UpdateTopicRequest
from topic_lake_api.app.controllers.topics.create import CreateTopicController
from topic_lake_api.app.controllers.topics.delete import DeleteTopicController
from topic_lake_api.app.controllers.topics.get import GetTopicController
from topic_lake_api.app.controllers.topics.list import ListTopicsController
from topic_lake_api.app.controllers.topics.update import UpdateTopicController

router = APIRouter(
    prefix='/topics',
    tags=['topics'],
    dependencies=[AuthenticationDependency]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=ListTopicsResponse)
async def list_topics(db: DBDependency, presenter: ListTopicsPresenterDependency,
                      topics_repository: TopicsRepositoryDependency):
    return await ListTopicsController(presenter, topics_repository).execute()


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateTopicResponse)
async def create_topic(db: DBDependency, request: Request, topic: CreateTopicRequest,
                       presenter: CreateTopicPresenterDependency, topics_repository: TopicsRepositoryDependency,
                       users_repository: UsersRepositoryDependency):
    return await CreateTopicController(presenter, topics_repository, users_repository).execute(
        request.user.id,
        topic.parent_topic_id,
        topic.content
    )


@router.get('/{topic_id}', status_code=status.HTTP_200_OK, response_model=GetTopicResponse)
async def get_topic(db: DBDependency, topic_id: int, presenter: GetTopicPresenterDependency,
                    topics_repository: TopicsRepositoryDependency):
    return await GetTopicController(presenter, topics_repository).execute(topic_id)


@router.delete('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(db: DBDependency, request: Request, topic_id: int,
                       topics_repository: TopicsRepositoryDependency, users_repository: UsersRepositoryDependency):
    await DeleteTopicController(topics_repository, users_repository).execute(
        request.user.id,
        topic_id
    )


@router.put('/{topic_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_topic(db: DBDependency, request: Request, topic_id: int, topic: UpdateTopicRequest,
                       topics_repository: TopicsRepositoryDependency, users_repository: UsersRepositoryDependency):
    return await UpdateTopicController(topics_repository, users_repository).execute(
        request.user.id,
        topic_id,
        topic.parent_topic_id,
        topic.content
    )

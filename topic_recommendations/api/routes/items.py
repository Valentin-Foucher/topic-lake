from fastapi import APIRouter
from starlette import status

from topic_recommendations.api.dependencies import ListItemsPresenterDependency, ItemsRepositoryDependency, \
    GetItemPresenterDependency, CreateItemPresenterDependency, TopicsRepositoryDependency, UsersRepositoryDependency
from topic_recommendations.api.models.items import CreateItemRequest, ListItemsResponse, GetItemResponse
from topic_recommendations.app.controllers.items.create import CreateItemController
from topic_recommendations.app.controllers.items.delete import DeleteItemController
from topic_recommendations.app.controllers.items.get import GetItemController
from topic_recommendations.app.controllers.items.list import ListItemsController

router = APIRouter(
    prefix="/topics/{topic_id}/items",
    tags=["items"]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=ListItemsResponse)
async def list_items(topic_id: int, presenter: ListItemsPresenterDependency,
                     items_repository: ItemsRepositoryDependency):
    return ListItemsController(presenter, items_repository).execute(topic_id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_item(topic_id: int, item: CreateItemRequest, presenter: CreateItemPresenterDependency,
                      items_repository: ItemsRepositoryDependency,
                      topics_repository: TopicsRepositoryDependency,
                      users_repository: UsersRepositoryDependency):
    return CreateItemController(presenter, items_repository, topics_repository, users_repository).execute(
        topic_id,
        item.user_id,
        item.content
    )


@router.get('/{item_id}', status_code=status.HTTP_200_OK, response_model=GetItemResponse)
async def get_item(topic_id: int, item_id: int, presenter: GetItemPresenterDependency,
                   items_repository: ItemsRepositoryDependency):
    return GetItemController(presenter, items_repository).execute(item_id)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(topic_id: int, item_id: int, items_repository: ItemsRepositoryDependency):
    DeleteItemController(items_repository).execute(item_id)

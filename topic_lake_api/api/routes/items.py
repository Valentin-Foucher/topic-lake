from fastapi import APIRouter
from starlette import status
from starlette.requests import Request

from topic_lake_api.api.dependencies import ListItemsPresenterDependency, ItemsRepositoryDependency, \
    GetItemPresenterDependency, CreateItemPresenterDependency, TopicsRepositoryDependency, UsersRepositoryDependency, \
    AuthenticationDependency, DBDependency
from topic_lake_api.api.models.items import CreateItemRequest, ListItemsResponse, GetItemResponse, UpdateItemRequest
from topic_lake_api.app.controllers.items.create import CreateItemController
from topic_lake_api.app.controllers.items.delete import DeleteItemController
from topic_lake_api.app.controllers.items.get import GetItemController
from topic_lake_api.app.controllers.items.list import ListItemsController
from topic_lake_api.app.controllers.items.update import UpdateItemController

router = APIRouter(
    prefix='/topics/{topic_id}/items',
    tags=['items'],
    dependencies=[AuthenticationDependency]
)


@router.get('', status_code=status.HTTP_200_OK, response_model=ListItemsResponse)
async def list_items(db: DBDependency, topic_id: int, presenter: ListItemsPresenterDependency,
                     items_repository: ItemsRepositoryDependency):
    return await ListItemsController(presenter, items_repository).execute(topic_id)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_item(db: DBDependency, request: Request, topic_id: int, item: CreateItemRequest,
                      presenter: CreateItemPresenterDependency,
                      items_repository: ItemsRepositoryDependency,
                      topics_repository: TopicsRepositoryDependency,
                      users_repository: UsersRepositoryDependency):
    return await CreateItemController(presenter, items_repository, topics_repository, users_repository).execute(
        topic_id,
        request.user.id,
        item.content,
        item.rank
    )


@router.get('/{item_id}', status_code=status.HTTP_200_OK, response_model=GetItemResponse)
async def get_item(db: DBDependency, item_id: int, presenter: GetItemPresenterDependency, items_repository: ItemsRepositoryDependency):
    return await GetItemController(presenter, items_repository).execute(item_id)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(db: DBDependency, request: Request, item_id: int, items_repository: ItemsRepositoryDependency):
    await DeleteItemController(items_repository).execute(
        request.user.id,
        item_id
    )


@router.put('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_item(db: DBDependency, request: Request, item_id: int, item: UpdateItemRequest,
                      items_repository: ItemsRepositoryDependency):
    await UpdateItemController(items_repository).execute(
        request.user.id,
        item_id,
        item.content,
        item.rank
    )

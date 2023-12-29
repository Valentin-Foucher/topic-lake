from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.items import CreateItemModel, ListItems, GetItem
from topic_recommendations.app.controllers.items.create import CreateItemController
from topic_recommendations.app.controllers.items.delete import DeleteItemController
from topic_recommendations.app.controllers.items.get import GetItemController
from topic_recommendations.app.controllers.items.list import ListItemsController
from topic_recommendations.app.presenters.items import ListItemsPresenter, GetItemPresenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

ItemsRepositoryDependency = \
    Annotated[IItemsRepository, Depends(partial(dependencies.get_repository, 'items'))]
ListItemsPresenterDependency = \
    Annotated[ListItemsPresenter, Depends(partial(dependencies.get_presenter, 'list'))]
GetItemPresenterDependency = \
    Annotated[GetItemPresenter, Depends(partial(dependencies.get_presenter, 'get'))]


@router.get('/', status_code=status.HTTP_200_OK, response_model=ListItems)
async def list_items(presenter: ListItemsPresenterDependency, items_repository: ItemsRepositoryDependency):
    return ListItemsController(presenter, items_repository).execute()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_item(item: CreateItemModel, items_repository: ItemsRepositoryDependency):
    CreateItemController(items_repository).execute(
        item.user_id,
        item.topic_id,
        item.content
    )


@router.get('/{item_id}', status_code=status.HTTP_200_OK, response_model=GetItem)
async def get_item(item_id: int, presenter: GetItemPresenterDependency, items_repository: ItemsRepositoryDependency):
    return GetItemController(presenter, items_repository).execute(item_id)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, items_repository: ItemsRepositoryDependency):
    DeleteItemController(items_repository).execute(item_id)

from functools import partial
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from topic_recommendations.api import dependencies
from topic_recommendations.api.models.items import CreateItemModel
from topic_recommendations.app.controllers.items import ItemsController
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

ItemsRepositoryDependency = \
    Annotated[IItemsRepository, Depends(partial(dependencies.get_repository, 'items'))]


@router.get('/', status_code=status.HTTP_200_OK)
async def list_items(items_repository: ItemsRepositoryDependency):
    return ItemsController() \
        .with_repository(items_repository) \
        .list()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_item(item: CreateItemModel, items_repository: ItemsRepositoryDependency):
    ItemsController() \
        .with_repository(items_repository) \
        .create(
            item.user_id,
            item.topic_id,
            item.content
        )


@router.get('/{item_id}', status_code=status.HTTP_200_OK)
async def get_item(item_id: int, items_repository: ItemsRepositoryDependency):
    return ItemsController() \
        .with_repository(items_repository) \
        .get(item_id)


@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, items_repository: ItemsRepositoryDependency):
    ItemsController() \
        .with_repository(items_repository) \
        .delete(item_id)

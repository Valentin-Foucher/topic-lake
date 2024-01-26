from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from topic_lake_api.api.utils.route_utils import ensure_authentication, ensure_authentication_if_authenticated
from topic_lake_api.app.presenters.connection import LogInPresenter
from topic_lake_api.app.presenters.items import GetItemPresenter, ListItemsPresenter, CreateItemPresenter
from topic_lake_api.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter, CreateTopicPresenter
from topic_lake_api.app.presenters.users import GetUserPresenter, CreateUserPresenter
from topic_lake_api.infra.db.core import get_db
from topic_lake_api.infra.repositories.access_tokens import AccessTokensRepository
from topic_lake_api.infra.repositories.items import ItemsRepository
from topic_lake_api.infra.repositories.topics import TopicsRepository
from topic_lake_api.infra.repositories.users import UsersRepository


# Database
DBDependency = Annotated[AsyncIterator[AsyncSession], Depends(get_db)]

# Repositories
UsersRepositoryDependency = Annotated[UsersRepository, Depends(UsersRepository)]
TopicsRepositoryDependency = Annotated[TopicsRepository, Depends(TopicsRepository)]
ItemsRepositoryDependency = Annotated[ItemsRepository, Depends(ItemsRepository)]
AccessTokensRepositoryDependency = Annotated[AccessTokensRepository, Depends(AccessTokensRepository)]

# Presenters
GetUserPresenterDependency = Annotated[GetUserPresenter, Depends(GetUserPresenter)]
CreateUserPresenterDependency = Annotated[CreateUserPresenter, Depends(CreateUserPresenter)]

ListTopicsPresenterDependency = Annotated[ListTopicsPresenter, Depends(ListTopicsPresenter)]
GetTopicPresenterDependency = Annotated[GetTopicPresenter, Depends(GetTopicPresenter)]
CreateTopicPresenterDependency = Annotated[CreateUserPresenter, Depends(CreateTopicPresenter)]

ListItemsPresenterDependency = Annotated[ListItemsPresenter, Depends(ListItemsPresenter)]
GetItemPresenterDependency = Annotated[GetItemPresenter, Depends(GetItemPresenter)]
CreateItemPresenterDependency = Annotated[CreateItemPresenter, Depends(CreateItemPresenter)]

LogInPresenterDependency = Annotated[LogInPresenter, Depends(LogInPresenter)]

# Authentication
AuthenticationDependency = Depends(ensure_authentication)
OptionalAuthenticationDependency = Depends(ensure_authentication_if_authenticated)

from typing import Annotated

from fastapi import Depends

from topic_lake_api.api.utils.route_utils import ensure_authentication
from topic_lake_api.app.presenters.connection import LogInPresenter
from topic_lake_api.app.presenters.items import GetItemPresenter, ListItemsPresenter, CreateItemPresenter
from topic_lake_api.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter, CreateTopicPresenter
from topic_lake_api.app.presenters.users import GetUserPresenter, CreateUserPresenter
from topic_lake_api.infra.repositories.access_tokens import AccessTokensRepository
from topic_lake_api.infra.repositories.items import ItemsRepository
from topic_lake_api.infra.repositories.topics import TopicsRepository
from topic_lake_api.infra.repositories.users import UsersRepository
from topic_lake_api.interactor.interfaces.repositories.access_tokens import IAccessTokensRepository
from topic_lake_api.interactor.interfaces.repositories.items import IItemsRepository
from topic_lake_api.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_lake_api.interactor.interfaces.repositories.users import IUsersRepository


# Repositories
UsersRepositoryDependency = Annotated[IUsersRepository, Depends(UsersRepository)]
TopicsRepositoryDependency = Annotated[ITopicsRepository, Depends(TopicsRepository)]
ItemsRepositoryDependency = Annotated[IItemsRepository, Depends(ItemsRepository)]
AccessTokensRepositoryDependency = Annotated[IAccessTokensRepository, Depends(AccessTokensRepository)]

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

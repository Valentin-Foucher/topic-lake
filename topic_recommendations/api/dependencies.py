from typing import Annotated

from fastapi import Depends

from topic_recommendations.app.presenters.items import GetItemPresenter, ListItemsPresenter, CreateItemPresenter
from topic_recommendations.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter, CreateTopicPresenter
from topic_recommendations.app.presenters.users import GetUserPresenter, CreateUserPresenter
from topic_recommendations.exceptions import InternalException
from topic_recommendations.infra.repositories.items import ItemsRepository
from topic_recommendations.infra.repositories.topics import TopicsRepository
from topic_recommendations.infra.repositories.users import UsersRepository
from topic_recommendations.interactor.interfaces.base import Repository, Presenter
from topic_recommendations.interactor.interfaces.repositories.items import IItemsRepository
from topic_recommendations.interactor.interfaces.repositories.topics import ITopicsRepository
from topic_recommendations.interactor.interfaces.repositories.users import IUsersRepository


# Repositories
UsersRepositoryDependency = Annotated[IUsersRepository, Depends(UsersRepository)]
TopicsRepositoryDependency = Annotated[ITopicsRepository, Depends(TopicsRepository)]
ItemsRepositoryDependency = Annotated[IItemsRepository, Depends(ItemsRepository)]


# Presenters
GetUserPresenterDependency = Annotated[GetUserPresenter, Depends(GetUserPresenter)]
CreateUserPresenterDependency = Annotated[CreateUserPresenter, Depends(CreateUserPresenter)]

ListTopicsPresenterDependency = Annotated[ListTopicsPresenter, Depends(ListTopicsPresenter)]
GetTopicPresenterDependency = Annotated[GetTopicPresenter, Depends(GetTopicPresenter)]
CreateTopicPresenterDependency = Annotated[CreateUserPresenter, Depends(CreateTopicPresenter)]

ListItemsPresenterDependency = Annotated[ListItemsPresenter, Depends(ListItemsPresenter)]
GetItemPresenterDependency = Annotated[GetItemPresenter, Depends(GetItemPresenter)]
CreateItemPresenterDependency = Annotated[CreateItemPresenter, Depends(CreateItemPresenter)]

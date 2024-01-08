from topic_recommendations.app.presenters.items import GetItemPresenter, ListItemsPresenter
from topic_recommendations.app.presenters.topics import ListTopicsPresenter, GetTopicPresenter
from topic_recommendations.app.presenters.users import GetUserPresenter, CreateUserPresenter
from topic_recommendations.exceptions import InternalException
from topic_recommendations.infra.repositories.items import ItemsRepository
from topic_recommendations.infra.repositories.topics import TopicsRepository
from topic_recommendations.infra.repositories.users import UsersRepository
from topic_recommendations.interactor.interfaces.base import Repository, Presenter

"""
As described here https://fastapi.tiangolo.com/tutorial/dependencies/, routers dependency injection should be defined
in a dedicated module. By convention, injector functions will be defined as get_<resource_type> 
"""


def get_repository(repository_name: str) -> Repository:
    match repository_name:
        case 'items':
            return ItemsRepository()
        case 'topics':
            return TopicsRepository()
        case 'users':
            return UsersRepository()
        case _:
            raise InternalException(f'Unknown collection name {repository_name}')


def get_presenter(view_name: str, action: str) -> Presenter:
    match view_name:
        case 'items':
            match action:
                case 'list':
                    return ListItemsPresenter()
                case 'get':
                    return GetItemPresenter()
        case 'topics':
            match action:
                case 'list':
                    return ListTopicsPresenter()
                case 'get':
                    return GetTopicPresenter()
        case 'users':
            match action:
                case 'get':
                    return GetUserPresenter()
                case 'create':
                    return CreateUserPresenter()
        case _:
            raise InternalException(f'Unknown collection name {view_name}')

    raise InternalException(f'Unknown action name for view {view_name}: {action}')

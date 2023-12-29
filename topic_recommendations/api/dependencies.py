from topic_recommendations.exceptions import InternalException
from topic_recommendations.infra.repositories.items import ItemsRepository
from topic_recommendations.infra.repositories.topics import TopicsRepository
from topic_recommendations.infra.repositories.users import UsersRepository
from topic_recommendations.interactor.interfaces.repositories.base import Repository
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

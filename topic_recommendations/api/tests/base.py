import os
from typing import Optional, Mapping, Union, Iterable
from unittest import IsolatedAsyncioTestCase

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, Response

from topic_recommendations.utils.object_utils import get_nested_element


os.environ['POSTGRES_TOPIC_RECOMMENDATIONS_CONNECTION_STRING'] = \
    'postgres://postgres:postgres@localhost:5432/topic-recommendations'

from topic_recommendations.api.main import app


class HttpTestCase(IsolatedAsyncioTestCase):
    _client: AsyncClient

    async def asyncSetUp(self):
        self._client = AsyncClient(app=app, base_url='http://localhost')
        self._lifespan_manager = LifespanManager(app)

    async def get(self, url: str, *args, **kwargs):
        async with self._lifespan_manager:
            return await self._client.get(url, *args, **kwargs)

    async def post(self, url: str, data: Optional[Mapping[str, Union[str, Iterable[str]]]] = None, **kwargs):
        async with self._lifespan_manager:
            return await self._client.post(url, json=data, **kwargs)

    async def delete(self, url: str, *args, **kwargs):
        async with self._lifespan_manager:
            return await self._client.delete(url, *args, **kwargs)

    async def put(self, url: str, data: Optional[Mapping[str, Union[str, Iterable[str]]]] = None, **kwargs):
        async with self._lifespan_manager:
            return await self._client.put(url, json=data, **kwargs)

    @staticmethod
    def get_data_from_response(response: Response, path: str):
        return get_nested_element(response.json(), path)

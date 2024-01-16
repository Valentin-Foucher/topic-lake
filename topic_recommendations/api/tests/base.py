import os
from typing import Optional, Mapping, Union, Iterable
from unittest import IsolatedAsyncioTestCase

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, Response

from topic_recommendations.infra.db.core import engine, Model, session
from topic_recommendations.infra.db.models import User
from topic_recommendations.utils.object_utils import get_nested_element


os.environ['POSTGRES_TOPIC_RECOMMENDATIONS_CONNECTION_STRING'] = \
    'postgresql://postgres:postgres@localhost:5432/topic-recommendations'

from topic_recommendations.api.main import app


class HttpTestCase(IsolatedAsyncioTestCase):
    _client: AsyncClient

    @classmethod
    def setUpClass(cls):
        cls._clear_db()
        Model.metadata.create_all(engine)
        cls._create_test_user()
        cls._client = AsyncClient(app=app, base_url='http://localhost')

    @classmethod
    def tearDownClass(cls):
        cls._clear_db()

    async def asyncSetUp(self):
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

    def validate_input_validation_error(self, response: Response, error_messages_and_input_for_fields):
        for err in self.get_data_from_response(response, 'detail'):
            self.assertIn(err['field'], error_messages_and_input_for_fields)
            message, value = error_messages_and_input_for_fields.pop(err['field'])
            self.assertEqual(err['value'], value)
            self.assertEqual(err['message'], message)

    @staticmethod
    def _clear_db():
        session.commit()
        Model.metadata.drop_all(engine)

    @staticmethod
    def _create_test_user(name='test_user', password='password123'):
        session.add(User(name=name, password=password))
        session.commit()
import os
from typing import Optional, Mapping, Union, Iterable, Any
from unittest import IsolatedAsyncioTestCase

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, Response

from topic_lake_api.interactor.utils.encryption_utils import hash_password
from topic_lake_api.infra.db.core import engine, Model, get_session
from topic_lake_api.infra.db.models import User, AccessToken
from topic_lake_api.utils.crypto_utils import encode_jwt
from topic_lake_api.utils.object_utils import get_nested_element

os.environ['TOPIC_LAKE_API_POSTGRES_CONNECTION_STRING'] = \
    'postgresql://postgres:postgres@localhost:5432/topic-lake'

from topic_lake_api.api.main import app


class HttpTestCase(IsolatedAsyncioTestCase):
    _client: AsyncClient
    token: str
    other_user_id: int
    user_id: int

    @classmethod
    def setUpClass(cls):
        cls._clear_db()
        Model.metadata.create_all(engine)
        u = cls._create_test_user()
        with get_session() as session:
            session.add(u)
            session.commit()

        cls._client = AsyncClient(app=app, base_url='http://localhost')

    @classmethod
    def tearDownClass(cls):
        cls._clear_db()

    async def asyncSetUp(self):
        self.login()
        self._lifespan_manager = LifespanManager(app)

    async def get(self, url: str, *args, without_token: bool = False, **kwargs):
        headers = self._get_headers(without_token)
        async with self._lifespan_manager:
            return await self._client.get(url, headers=headers, *args, **kwargs)

    async def post(self, url: str, data: Optional[Mapping[str, Union[Any, Iterable[Any]]]] = None,
                   without_token: bool = False, **kwargs):
        headers = self._get_headers(without_token)
        async with self._lifespan_manager:
            return await self._client.post(url, headers=headers, json=data, **kwargs)

    async def delete(self, url: str, *args, without_token: bool = False, **kwargs):
        headers = self._get_headers(without_token)
        async with self._lifespan_manager:
            return await self._client.delete(url, headers=headers, *args, **kwargs)

    async def put(self, url: str, data: Optional[Mapping[str, Union[Any, Iterable[Any]]]] = None,
                  without_token: bool = False, **kwargs):
        headers = self._get_headers(without_token)
        async with self._lifespan_manager:
            return await self._client.put(url, headers=headers, json=data, **kwargs)

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
        with get_session() as session:
            session.commit()
            Model.metadata.drop_all(engine)

    @staticmethod
    def _create_test_user(name='test_user', password='password123', admin=False):
        return User(name=name, password=hash_password(password), admin=admin)

    def _get_headers(self, without_token: bool):
        headers = {}
        if not without_token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def login(self, user_id=1):
        self.token = encode_jwt(user_id)
        self.user_id = user_id

        token = AccessToken(value=self.token, user_id=user_id)
        with get_session() as session:
            session.add(token)
            session.commit()

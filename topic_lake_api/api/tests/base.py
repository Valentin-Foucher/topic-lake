from typing import Optional, Mapping, Union, Iterable, Any

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient, Response
from sqlalchemy.ext.asyncio import AsyncSession

from topic_lake_api.interactor.utils.encryption_utils import hash_password
from topic_lake_api.infra.db.models import User, AccessToken
from topic_lake_api.utils.crypto_utils import encode_jwt
from topic_lake_api.utils.object_utils import get_nested_element


class HttpTestCase:
    _client: AsyncClient
    _lifespan_manager: LifespanManager
    token: str
    other_user_id: int
    user_id: int
    should_login: bool = True

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def client(self, app):
        self._client = AsyncClient(app=app, base_url='http://localhost')

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def lifespan_manager(self, app):
        self._lifespan_manager = LifespanManager(app, 10000, 10000)

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def user(self, db):
        await self.create_test_user(db)

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def login_user(self, db):
        if self.should_login:
            await self.login(db)

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
        return await self._client.put(url, headers=headers, json=data, **kwargs)

    @staticmethod
    def get_data_from_response(response: Response, path: str):
        return get_nested_element(response.json(), path)

    def validate_input_validation_error(self, response: Response, error_messages_and_input_for_fields):
        for err in self.get_data_from_response(response, 'detail'):
            assert err['field'] in error_messages_and_input_for_fields
            message, value = error_messages_and_input_for_fields.pop(err['field'])
            assert err['value'] == value
            assert err['message'] == message

    @staticmethod
    async def create_test_user(db: AsyncSession, name='test_user', password='password123', admin=False):
        u = User(name=name, password=hash_password(password), admin=admin)
        db.add(u)
        await db.commit()
        await db.flush()
        return u

    def _get_headers(self, without_token: bool):
        headers = {}
        if not without_token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    async def login(self, db, user_id=1):
        self.token = encode_jwt(user_id)
        self.user_id = user_id
        token = AccessToken(value=self.token, user_id=user_id)
        db.add(token)
        await db.commit()

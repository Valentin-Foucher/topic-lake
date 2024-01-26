from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.infra.db.models import User


@pytest.mark.asyncio
class TestUsers(HttpTestCase):
    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def clear_db(self, user, db, event_loop):
        await db.execute(
            delete(User).filter(User.name != 'test_user')
        )

    async def _create_user(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/api/v1/users', {
            'username': 'user',
            'password': 'password123',
            **overriding_dict
        },
                                   without_token=True)

        assert status_code == response.status_code
        if status_code == 201:
            assert isinstance(self.get_data_from_response(response, 'id'), int)
        elif status_code == 422:
            field, value = next(iter(overriding_dict.items()))
            self.validate_input_validation_error(response, {
                field: [error_message, value]
            })
        else:
            assert error_message == self.get_data_from_response(response, 'detail')

        return response

    @staticmethod
    def _assert_user(user: dict[str, Any]):
        assert isinstance(user['id'], int)
        assert 'user' == user['name']
        assert 'password' not in user

    async def test_create_with_invalid_username(self):
        await self._create_user(username=111,
                                status_code=422,
                                error_message='Input should be a valid string')
        await self._create_user(username='a' * 3,
                                status_code=422,
                                error_message='String should have at least 4 characters')
        await self._create_user(username='a' * 65,
                                status_code=422,
                                error_message='String should have at most 64 characters')

    async def test_create_with_invalid_password(self):
        await self._create_user(password=111,
                                status_code=422,
                                error_message='Input should be a valid string')
        await self._create_user(password='a' * 7,
                                status_code=422,
                                error_message='String should have at least 8 characters')
        await self._create_user(password='a' * 65,
                                status_code=422,
                                error_message='String should have at most 64 characters')

    async def test_create_user(self):
        await self._create_user()

    async def test_get_user(self, db):
        response = await self._create_user()
        inserted_id = self.get_data_from_response(response, 'id')
        await self.login(db, inserted_id)

        response = await self.get('/api/v1/users/self')
        assert 200 == response.status_code
        self._assert_user(self.get_data_from_response(response, 'user'))

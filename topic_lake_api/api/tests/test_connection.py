from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import select, delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.infra.db.models import AccessToken


@pytest.mark.asyncio
class TestConnection(HttpTestCase):
    should_login = False

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def clear_db(self, user, db, event_loop):
        await db.execute(
            delete(AccessToken)
        )

    async def _login(self, status_code=200, error_message='', **overriding_dict):
        response = await self.post('/api/v1/login', {
            'username': 'test_user',
            'password': 'password123',
            **overriding_dict
        },
                                   without_token=True)

        assert status_code == response.status_code
        if status_code == 200:
            data = response.json()
            assert isinstance(data['token'], str)
            assert isinstance(data['user_id'], int)
        elif status_code == 422:
            field, value = next(iter(overriding_dict.items()))
            self.validate_input_validation_error(response, {
                field: [error_message, value]
            })
        else:
            assert error_message == self.get_data_from_response(response, 'detail')

        return response

    async def _logout(self, status_code=200, error_message='', without_token=False):
        response = await self.post('/api/v1/logout', {}, without_token=without_token)

        assert status_code == response.status_code

        if status_code != 200:
            assert error_message == self.get_data_from_response(response, 'detail')

        return response

    async def test_login_with_invalid_username(self):
        await self._login(username=111,
                          status_code=422,
                          error_message='Input should be a valid string')

        await self._login(username='not_existent',
                          status_code=400,
                          error_message='Invalid credentials')

    async def test_login_with_invalid_password(self):
        await self._login(password=111,
                          status_code=422,
                          error_message='Input should be a valid string')

        await self._login(password='not_the_correct_password',
                          status_code=400,
                          error_message='Invalid credentials')

    async def test_login(self):
        await self._login()

    async def test_login_several_times(self):
        response = await self._login()
        token = self.get_data_from_response(response, 'token')
        response = await self._login()
        token2 = self.get_data_from_response(response, 'token')
        assert token == token2

    async def test_login_after_token_expiration(self, db):
        old_token = '123456'
        t = AccessToken(value=old_token, user_id=1, creation_date=datetime.utcnow() - timedelta(hours=1))
        db.add(t)
        await db.commit()

        response = await self._login()
        new_token = self.get_data_from_response(response, 'token')
        assert old_token != new_token

    async def test_logout(self, db):
        await self._logout(without_token=True)
        tokens = (await db.scalars(
            select(AccessToken)
            .where(AccessToken.user_id == 1)
        )).all()
        assert 0 == len(tokens)

        await self.login(db)
        tokens = (await db.scalars(
            select(AccessToken)
            .where(AccessToken.user_id == 1)
        )).all()
        assert 1 == len(tokens)
        token = tokens[0]
        assert token.revoked is False

        await self._logout(without_token=False)
        await db.refresh(token)
        assert token.revoked is True

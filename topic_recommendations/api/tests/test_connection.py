from datetime import datetime, timedelta

from sqlalchemy import select, and_

from topic_recommendations.api.tests.base import HttpTestCase
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import AccessToken


class ItemsTestCase(HttpTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        AccessToken.query.delete()

    async def _login(self, status_code=200, error_message='', **overriding_dict):
        response = await self.post('/login', {
            'username': 'test_user',
            'password': 'password123',
            **overriding_dict
        })

        self.assertEqual(status_code, response.status_code)
        if status_code == 200:
            token = self.get_data_from_response(response, 'token')
            self.assertIsInstance(token, str)
            self.assertEqual(32, len(token))
        elif status_code == 422:
            field, value = next(iter(overriding_dict.items()))
            self.validate_input_validation_error(response, {
                field: [error_message, value]
            })
        else:
            self.assertEqual(error_message, self.get_data_from_response(response, 'detail'))

        return response

    async def _logout(self, status_code=200, error_message='', **overriding_dict):
        response = await self.post('/logout', {
            'user_id': 1,
            **overriding_dict
        })

        self.assertEqual(status_code, response.status_code)

        if status_code == 422:
            field, value = next(iter(overriding_dict.items()))
            self.validate_input_validation_error(response, {
                field: [error_message, value]
            })
        elif status_code != 200:
            self.assertEqual(error_message, self.get_data_from_response(response, 'detail'))

        return response

    async def test_login_with_invalid_username(self):
        await self._login(username=111,
                          status_code=422,
                          error_message='Input should be a valid string')

        await self._login(username='not_existent',
                          status_code=404,
                          error_message='User "not_existent" does not exist')

    async def test_login_with_invalid_password(self):
        await self._login(password=111,
                          status_code=422,
                          error_message='Input should be a valid string')

        await self._login(password='not_the_correct_password',
                          status_code=400,
                          error_message='Password is incorrect')

    async def test_login(self):
        await self._login()

    async def test_login_several_times(self):
        response = await self._login()
        token = self.get_data_from_response(response, 'token')
        response = await self._login()
        token2 = self.get_data_from_response(response, 'token')
        self.assertEqual(token, token2)

    async def test_login_after_token_expiration(self):
        old_token = '123456'
        t = AccessToken(value=old_token, user_id=1, creation_date=datetime.utcnow() - timedelta(hours=1))
        session.add(t)
        session.commit()

        response = await self._login()
        new_token = self.get_data_from_response(response, 'token')
        self.assertNotEqual(old_token, new_token)

    async def test_logout_with_invalid_user_id(self):
        await self._logout(user_id='invalid user id', status_code=422,
                           error_message='Input should be a valid integer, unable to parse string as an integer')
        await self._logout(user_id=123456, status_code=404, error_message='User 123456 does not exist')

    async def test_logout(self):
        await self._logout()
        tokens = session.scalars(
            select(AccessToken)
            .where(AccessToken.user_id == 1)
        ).all()
        self.assertEqual(0, len(tokens))

        await self._login()
        tokens = session.scalars(
            select(AccessToken)
            .where(AccessToken.user_id == 1)
        ).all()
        self.assertEqual(1, len(tokens))
        self.assertFalse(tokens[0].revoked)

        await self._logout()
        tokens = session.scalars(
            select(AccessToken)
            .where(AccessToken.user_id == 1)
        ).all()
        self.assertEqual(1, len(tokens))
        self.assertTrue(tokens[0].revoked)

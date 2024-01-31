from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.infra.db.core import get_session
from topic_lake_api.infra.db.models import User


class UsersTestCase(HttpTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        with get_session() as session:
            session.execute(
                User.__table__.delete()
                .where(User.id != 1)
            )

    async def _create_user(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/api/v1/users', {
            'username': 'user',
            'password': 'password123',
            **overriding_dict
        },
                                   without_token=True)

        self.assertEqual(status_code, response.status_code)
        if status_code == 201:
            self.assertIsInstance(self.get_data_from_response(response, 'id'), int)
        elif status_code == 422:
            field, value = next(iter(overriding_dict.items()))
            self.validate_input_validation_error(response, {
                field: [error_message, value]
            })
        else:
            self.assertEqual(error_message, self.get_data_from_response(response, 'detail'))

        return response

    def _assert_user(self, user):
        self.assertIsInstance(user['id'], int)
        self.assertEqual('user', user['name'])
        self.assertNotIn('password', user)

    async def test_create_with_invalid_username(self):
        await self._create_user(username=111,
                                status_code=422,
                                error_message='Input should be a valid string')
        await self._create_user(username='a' * 2,
                                status_code=422,
                                error_message='String should have at least 3 characters')
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

    async def test_get_user(self):
        response = await self._create_user()
        inserted_id = self.get_data_from_response(response, 'id')
        self.login(inserted_id)

        response = await self.get('/api/v1/users/self')
        self.assertEqual(200, response.status_code)
        self._assert_user(self.get_data_from_response(response, 'user'))

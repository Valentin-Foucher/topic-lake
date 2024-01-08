from topic_recommendations.api.tests.base import HttpTestCase
from topic_recommendations.infra.db.models import User


class UsersTestCase(HttpTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        User.query.delete()

    async def _create_user(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/users', {
            'name': 'user',
            'password': 'password123',
            **overriding_dict
        })

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

    async def test_create_with_invalid_name(self):
        await self._create_user(name=111,
                                status_code=422,
                                error_message='Input should be a valid string')

    async def test_create_with_invalid_password(self):
        await self._create_user(password=111,
                                status_code=422,
                                error_message='Input should be a valid string')

    async def test_create_user(self):
        await self._create_user()

    async def test_get_unknown_user(self):
        response = await self.get('/users/123456')
        self.assertEqual(404, response.status_code)
        self.assertEqual('User 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_get_user(self):
        response = await self._create_user()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/users/{inserted_it}')
        self.assertEqual(200, response.status_code)
        self._assert_user(self.get_data_from_response(response, 'user'))

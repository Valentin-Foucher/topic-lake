from topic_recommendations.api.tests.base import HttpTestCase
from topic_recommendations.infra.db.models import Topic


class TopicsTestCase(HttpTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        Topic.query.delete()

    async def _create_topic(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/topics', {
            'content': 'Holiday destinations',
            'user_id': 1,
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

    def _assert_topic(self, topic):
        self.assertIsInstance(topic['id'], int)
        self.assertEqual('Holiday destinations', topic['content'])
        self.assertEqual(1, topic['user_id'])

    async def test_create_with_invalid_content(self):
        await self._create_topic(content=111,
                                 status_code=422,
                                 error_message='Input should be a valid string')

    async def test_create_with_invalid_user_id(self):
        await self._create_topic(user_id='not a valid id',
                                 status_code=422,
                                 error_message='Input should be a valid integer, unable to parse string as an integer')
        await self._create_topic(user_id=13,
                                 status_code=404,
                                 error_message='User 13 does not exist')

    async def test_create_topic(self):
        await self._create_topic()

    async def test_get_unknown_topic(self):
        response = await self.get('/topics/123456')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Topic 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_get_topic(self):
        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/topics/{inserted_it}')
        self.assertEqual(200, response.status_code)
        self._assert_topic(self.get_data_from_response(response, 'topic'))

    async def test_delete_topic(self):
        response = await self.delete('/topics/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Topic 1 does not exist', self.get_data_from_response(response, 'detail'))

        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/topics/{inserted_it}')
        self.assertEqual(204, response.status_code)

        response = await self.get('/topics/1')
        self.assertEqual(404, response.status_code)
from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.api.tests.decorators import with_another_user
from topic_lake_api.infra.db.models import Topic


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
        if topic['parent_topic_id'] is not None:
            self.assertIsInstance(topic['parent_topic_id'], int)
        self.assertIsInstance(topic['sub_topics'], list)

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

    async def test_create_topic_with_invalid_parent_id(self):
        await self._create_topic(parent_topic_id=123,
                                 status_code=404,
                                 error_message='Topic 123 does not exist')

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

    async def test_list_topics(self):
        response = await self.get('/topics')
        self.assertEqual(0, len(self.get_data_from_response(response, 'topics')))

        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        response = await self.get('/topics')
        self.assertEqual(1, len(self.get_data_from_response(response, 'topics')))

        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        response = await self.get('/topics')
        self.assertEqual(2, len(self.get_data_from_response(response, 'topics')))

    async def test_create_sub_topic(self):
        """
        structure:
        parent:
            first child:
                first great child
            second child
        """
        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        parent_id = self.get_data_from_response(response, 'id')
        
        response = await self._create_topic(parent_topic_id=parent_id)
        self.assertEqual(201, response.status_code)
        first_child_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=parent_id)
        self.assertEqual(201, response.status_code)
        second_child_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=first_child_id)
        self.assertEqual(201, response.status_code)
        first_great_child_id = self.get_data_from_response(response, 'id')

        response = await self.get(f'/topics/{parent_id}')
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/topics/{first_child_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(parent_id, self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/topics/{second_child_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(parent_id, self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/topics/{first_great_child_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(first_child_id, self.get_data_from_response(response, 'topic.parent_topic_id'))

    async def test_get_topics_hierarchy(self):
        """
        structure:
        first_root:
            child
        second_root
        """
        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        first_root_topic_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        second_root_topic_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=first_root_topic_id)
        self.assertEqual(201, response.status_code)
        child_topic_id = self.get_data_from_response(response, 'id')

        response = await self.get('/topics')
        self.assertEqual(200, response.status_code)

        self._assert_topic(self.get_data_from_response(response, 'topics.0'))
        self._assert_topic(self.get_data_from_response(response, 'topics.1'))
        self._assert_topic(self.get_data_from_response(response, 'topics.0.sub_topics.0'))
        self.assertEqual(first_root_topic_id, self.get_data_from_response(response, 'topics.0.id'))
        self.assertEqual(second_root_topic_id, self.get_data_from_response(response, 'topics.1.id'))
        self.assertEqual(child_topic_id, self.get_data_from_response(response, 'topics.0.sub_topics.0.id'))

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_topic(self):
        # creating topic as main user
        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        self.login(self.other_user_id)
        response = await self.delete(f'/topics/{topic_id}')
        self.assertEqual(404, response.status_code)
        self.assertEqual(f'Topic {topic_id} does not exist', self.get_data_from_response(response, 'detail'))

        # logging back in as main user
        self.login()
        response = await self.delete(f'/topics/{topic_id}')
        self.assertEqual(204, response.status_code)

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_topic(self):
        # creating topic as main user
        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        # logging in as admin
        self.login(self.other_user_id)
        response = await self.delete(f'/topics/{topic_id}')
        self.assertEqual(204, response.status_code)

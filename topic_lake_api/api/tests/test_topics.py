import uuid
from pprint import pprint

from sqlalchemy import delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.api.tests.decorators import with_another_user
from topic_lake_api.infra.db.core import get_session
from topic_lake_api.infra.db.models import Topic


class TopicsTestCase(HttpTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        with get_session() as session:
            session.execute(
                delete(Topic)
            )

    async def _create_topic(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/api/v1/topics', {
            'content': uuid.uuid4().hex,
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
        self.assertIsInstance(topic['content'], str)
        self.assertEqual(1, topic['user_id'])
        if topic['parent_topic_id'] is not None:
            self.assertIsInstance(topic['parent_topic_id'], int)
        self.assertIsInstance(topic['sub_topics'], list)

    async def test_create_with_invalid_content(self):
        await self._create_topic(content=111,
                                 status_code=422,
                                 error_message='Input should be a valid string')
        await self._create_topic(content='a' * 2,
                                 status_code=422,
                                 error_message='String should have at least 3 characters')
        await self._create_topic(content='a' * 257,
                                 status_code=422,
                                 error_message='String should have at most 256 characters')

    async def test_create_topic_with_invalid_parent_id(self):
        await self._create_topic(parent_topic_id=123,
                                 status_code=404,
                                 error_message='Topic 123 does not exist')

    async def test_recreate_already_existing_topic(self):
        content = 'already existing topic'
        await self._create_topic(content=content)
        await self._create_topic(content=content,
                                 status_code=400,
                                 error_message='This topic already exists')

    async def test_create_topic(self):
        await self._create_topic()

    async def test_get_unknown_topic(self):
        response = await self.get('/api/v1/topics/123456')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Topic 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_get_topic(self):
        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/api/v1/topics/{inserted_it}')
        self.assertEqual(200, response.status_code)
        self._assert_topic(self.get_data_from_response(response, 'topic'))

    async def test_delete_topic(self):
        response = await self.delete('/api/v1/topics/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Topic 1 does not exist', self.get_data_from_response(response, 'detail'))

        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/api/v1/topics/{inserted_it}')
        self.assertEqual(204, response.status_code)

        response = await self.get('/api/v1/topics/1')
        self.assertEqual(404, response.status_code)

    async def test_list_topics(self):
        response = await self.get('/api/v1/topics')
        self.assertEqual(0, len(self.get_data_from_response(response, 'topics')))

        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        response = await self.get('/api/v1/topics')
        self.assertEqual(1, len(self.get_data_from_response(response, 'topics')))

        response = await self._create_topic()
        self.assertEqual(201, response.status_code)
        response = await self.get('/api/v1/topics')
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

        response = await self.get(f'/api/v1/topics/{parent_id}')
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/api/v1/topics/{first_child_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(parent_id, self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/api/v1/topics/{second_child_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(parent_id, self.get_data_from_response(response, 'topic.parent_topic_id'))

        response = await self.get(f'/api/v1/topics/{first_great_child_id}')
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

        response = await self.get('/api/v1/topics')
        self.assertEqual(200, response.status_code)

        self._assert_topic(self.get_data_from_response(response, 'topics.0'))
        self._assert_topic(self.get_data_from_response(response, 'topics.1'))
        print(pprint(response.json()))
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
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        self.assertEqual(403, response.status_code)
        self.assertEqual(f'This topic hierarchy was not entirely created by user {self.other_user_id}',
                         self.get_data_from_response(response, 'detail'))

        # logging back in as main user
        self.login()
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        self.assertEqual(204, response.status_code)

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_topic(self):
        # creating topic as main user
        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        # logging in as admin
        self.login(self.other_user_id)
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        self.assertEqual(204, response.status_code)

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_topic_if_he_does_not_own_the_hierarchy(self):
        # logging in as main user
        response = await self._create_topic()
        root_topic_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        self.login(self.other_user_id)
        await self._create_topic(parent_topic_id=root_topic_id)

        # logging in back as main user
        self.login()
        response = await self.delete(f'/api/v1/topics/{root_topic_id}')
        self.assertEqual(403, response.status_code)
        self.assertEqual(f'This topic hierarchy was not entirely created by user {self.user_id}',
                         self.get_data_from_response(response, 'detail'))

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_topic_even_if_he_does_not_own_the_hierarchy(self):
        # logging in as admin
        self.login(self.other_user_id)
        response = await self._create_topic()
        root_topic_id = self.get_data_from_response(response, 'id')

        # logging in as main user
        self.login()
        await self._create_topic(parent_topic_id=root_topic_id)

        # logging in back as admin
        self.login(self.other_user_id)
        response = await self.delete(f'/api/v1/topics/{root_topic_id}')
        self.assertEqual(204, response.status_code)

    @with_another_user()
    async def test_update_topic_belonging_to_another_user(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        self.login(self.other_user_id)
        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': None
        })
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            f'This topic is not owned by user {self.other_user_id}',
            self.get_data_from_response(response, 'detail')
        )

    @with_another_user(admin=True)
    async def test_update_topic_belonging_to_another_user_as_an_admin(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        self.login(self.other_user_id)
        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': None
        })
        self.assertEqual(204, response.status_code)

    async def test_update_topic_with_invalid_parent_topic_id(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': 123456
        })
        self.assertEqual(404, response.status_code)
        self.assertEqual('Topic 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_update_topic(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')
        response = await self._create_topic()
        parent_topic_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': parent_topic_id
        })
        self.assertEqual(204, response.status_code)

        response = await self.get(f'/api/v1/topics/{topic_to_update_id}')
        topic = self.get_data_from_response(response, 'topic')
        self.assertEqual('new content', topic['content'])
        self.assertEqual(1, topic['user_id'])
        self.assertEqual(parent_topic_id, topic['parent_topic_id'])
        self.assertEqual([], topic['sub_topics'])

    async def test_update_topic_but_a_similar_one_already_exists(self):
        content = 'already existing topic'
        await self._create_topic(content=content)

        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_id}', {
            'content': content,
            'parent_topic_id': None
        })
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Cannot move or rename this topic, a similar topic already exists',
            self.get_data_from_response(response, 'detail')
        )

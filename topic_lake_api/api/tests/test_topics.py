import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.api.tests.decorators import with_another_user
from topic_lake_api.infra.db.models import Topic


@pytest.mark.asyncio
class TestTopics(HttpTestCase):
    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def clear_db(self, user, db, event_loop):
        await db.execute(
            delete(Topic)
        )

    async def _create_topic(self, status_code=201, error_message='', **overriding_dict):
        response = await self.post('/api/v1/topics', {
            'content': uuid.uuid4().hex,
            **overriding_dict
        })

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
    def _assert_topic(topic):
        assert isinstance(topic['id'], int)
        assert isinstance(topic['content'], str)
        assert 1 == topic['user_id']
        if topic['parent_topic_id'] is not None:
            assert isinstance(topic['parent_topic_id'], int)
        assert isinstance(topic['sub_topics'], list)

    async def test_create_with_invalid_content(self):
        await self._create_topic(content=111,
                                 status_code=422,
                                 error_message='Input should be a valid string')
        await self._create_topic(content='a',
                                 status_code=422,
                                 error_message='String should have at least 4 characters')
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
        assert 404 == response.status_code
        assert 'Topic 123456 does not exist' == self.get_data_from_response(response, 'detail')

    async def test_get_topic(self):
        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/api/v1/topics/{inserted_it}')
        assert 200 == response.status_code
        self._assert_topic(self.get_data_from_response(response, 'topic'))

    async def test_delete_topic(self):
        response = await self.delete('/api/v1/topics/1')
        assert 404 == response.status_code
        assert 'Topic 1 does not exist' == self.get_data_from_response(response, 'detail')

        response = await self._create_topic()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/api/v1/topics/{inserted_it}')
        assert 204 == response.status_code

        response = await self.get('/api/v1/topics/1')
        assert 404 == response.status_code

    async def test_list_topics(self):
        response = await self.get('/api/v1/topics')
        assert 200 == response.status_code
        assert 0 == len(self.get_data_from_response(response, 'topics'))

        response = await self._create_topic()
        assert 201 == response.status_code
        response = await self.get('/api/v1/topics')
        assert 200 == response.status_code
        assert 1 == len(self.get_data_from_response(response, 'topics'))

        response = await self._create_topic()
        assert 201 == response.status_code
        response = await self.get('/api/v1/topics')
        assert 200 == response.status_code
        assert 2 == len(self.get_data_from_response(response, 'topics'))

    async def test_create_sub_topic(self):
        """
        structure:
        parent:
            first child:
                first great child
            second child
        """
        response = await self._create_topic()
        assert 201 == response.status_code
        parent_id = self.get_data_from_response(response, 'id')
        
        response = await self._create_topic(parent_topic_id=parent_id)
        assert 201 == response.status_code
        first_child_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=parent_id)
        assert 201 == response.status_code
        second_child_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=first_child_id)
        assert 201 == response.status_code
        first_great_child_id = self.get_data_from_response(response, 'id')

        response = await self.get(f'/api/v1/topics/{parent_id}')
        assert 200 == response.status_code
        assert self.get_data_from_response(response, 'topic.parent_topic_id') is None

        response = await self.get(f'/api/v1/topics/{first_child_id}')
        assert 200 == response.status_code
        assert parent_id == self.get_data_from_response(response, 'topic.parent_topic_id')

        response = await self.get(f'/api/v1/topics/{second_child_id}')
        assert 200 == response.status_code
        assert parent_id == self.get_data_from_response(response, 'topic.parent_topic_id')

        response = await self.get(f'/api/v1/topics/{first_great_child_id}')
        assert 200 == response.status_code
        assert first_child_id == self.get_data_from_response(response, 'topic.parent_topic_id')

    async def test_get_topics_hierarchy(self):
        """
        structure:
        first_root:
            child
        second_root
        """
        response = await self._create_topic()
        assert 201 == response.status_code
        first_root_topic_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic()
        assert 201 == response.status_code
        second_root_topic_id = self.get_data_from_response(response, 'id')

        response = await self._create_topic(parent_topic_id=first_root_topic_id)
        assert 201 == response.status_code
        child_topic_id = self.get_data_from_response(response, 'id')

        response = await self.get('/api/v1/topics')
        assert 200 == response.status_code

        self._assert_topic(self.get_data_from_response(response, 'topics.0'))
        self._assert_topic(self.get_data_from_response(response, 'topics.1'))
        self._assert_topic(self.get_data_from_response(response, 'topics.0.sub_topics.0'))
        assert first_root_topic_id == self.get_data_from_response(response, 'topics.0.id')
        assert second_root_topic_id == self.get_data_from_response(response, 'topics.1.id')
        assert child_topic_id == self.get_data_from_response(response, 'topics.0.sub_topics.0.id')

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_topic(self, db):
        # creating topic as main user
        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        await self.login(db, self.other_user_id)
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        assert 403 == response.status_code
        assert f'This topic hierarchy was not entirely created by user {self.other_user_id}' == \
               self.get_data_from_response(response, 'detail')

        # logging back in as main user
        await self.login(db)
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        assert 204 == response.status_code

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_topic(self, db):
        # creating topic as main user
        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        # logging in as admin
        await self.login(db, self.other_user_id)
        response = await self.delete(f'/api/v1/topics/{topic_id}')
        assert 204 == response.status_code

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_topic_if_he_does_not_own_the_hierarchy(self, db):
        # logging in as main user
        response = await self._create_topic()
        root_topic_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        await self.login(db, self.other_user_id)
        await self._create_topic(parent_topic_id=root_topic_id)

        # logging in back as main user
        await self.login(db)
        response = await self.delete(f'/api/v1/topics/{root_topic_id}')
        assert 403 == response.status_code 
        assert f'This topic hierarchy was not entirely created by user {self.user_id}' == \
               self.get_data_from_response(response, 'detail')

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_topic_even_if_he_does_not_own_the_hierarchy(self, db):
        # logging in as admin
        await self.login(db, self.other_user_id)
        response = await self._create_topic()
        root_topic_id = self.get_data_from_response(response, 'id')

        # logging in as main user
        await self.login(db)
        await self._create_topic(parent_topic_id=root_topic_id)

        # logging in back as admin
        await self.login(db, self.other_user_id)
        response = await self.delete(f'/api/v1/topics/{root_topic_id}')
        assert 204 == response.status_code

    @with_another_user()
    async def test_update_topic_belonging_to_another_user(self, db):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        await self.login(db, self.other_user_id)
        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': None
        })
        assert 403 == response.status_code 
        assert f'This topic is not owned by user {self.other_user_id}' == \
               self.get_data_from_response(response, 'detail')

    @with_another_user(admin=True)
    async def test_update_topic_belonging_to_another_user_as_an_admin(self, db):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        await self.login(db, self.other_user_id)
        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': None
        })
        assert 204 == response.status_code

    async def test_update_topic_with_invalid_parent_topic_id(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': 123456
        })
        assert 404 == response.status_code
        assert 'Topic 123456 does not exist' == self.get_data_from_response(response, 'detail')

    async def test_update_topic(self):
        response = await self._create_topic()
        topic_to_update_id = self.get_data_from_response(response, 'id')
        response = await self._create_topic()
        parent_topic_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_to_update_id}', {
            'content': 'new content',
            'parent_topic_id': parent_topic_id
        })
        assert 204 == response.status_code

        response = await self.get(f'/api/v1/topics/{topic_to_update_id}')
        topic = self.get_data_from_response(response, 'topic')
        assert 'new content' == topic['content']
        assert 1 == topic['user_id']
        assert parent_topic_id == topic['parent_topic_id']
        assert [] == topic['sub_topics']

    async def test_update_topic_but_a_similar_one_already_exists(self):
        content = 'already existing topic'
        await self._create_topic(content=content)

        response = await self._create_topic()
        topic_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/{topic_id}', {
            'content': content,
            'parent_topic_id': None
        })
        assert 400 == response.status_code
        assert 'This topic already exists' == self.get_data_from_response(response, 'detail')

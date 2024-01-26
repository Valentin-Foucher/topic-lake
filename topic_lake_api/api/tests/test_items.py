import pytest
import pytest_asyncio
from sqlalchemy import select, delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.api.tests.decorators import with_another_user
from topic_lake_api.infra.db.models import Item, Topic


@pytest.mark.asyncio
class TestItems(HttpTestCase):
    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def add_topic(self, user, db, event_loop):
        db.add(Topic(content='Holiday destinations', user_id=1))
        await db.commit()

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def clear_db(self, user, db, event_loop):
        await db.execute(
            delete(Item)
        )

    async def _create_item(self, status_code=201, error_message='', topic_id=1, **overriding_dict):
        response = await self.post(f'/api/v1/topics/{topic_id}/items', {
            'content': 'Ibiza',
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
    def _assert_item(item):
        assert isinstance(item['id'], int)
        assert 'Ibiza' == item['content']
        assert 'test_user' == item['user_name']
        assert 'Holiday destinations' == item['topic_content']

    async def test_create_with_invalid_content(self):
        await self._create_item(content=111,
                                status_code=422,
                                error_message='Input should be a valid string')
        await self._create_item(content='a',
                                status_code=422,
                                error_message='String should have at least 4 characters')
        await self._create_item(content='a' * 257,
                                status_code=422,
                                error_message='String should have at most 256 characters')

    async def test_create_item(self):
        await self._create_item()

    async def test_get_unknown_item(self):
        response = await self.get('/api/v1/topics/1/items/123456')
        assert 404 == response.status_code
        assert 'Item 123456 does not exist' == self.get_data_from_response(response, 'detail')

    async def test_get_item(self):
        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/api/v1/topics/1/items/{inserted_it}')
        assert 200 == response.status_code
        self._assert_item(self.get_data_from_response(response, 'item'))

    async def test_delete_item(self):
        response = await self.delete('/api/v1/topics/1/items/1')
        assert 404 == response.status_code
        assert 'Item 1 does not exist' == self.get_data_from_response(response, 'detail')

        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/api/v1/topics/1/items/{inserted_it}')
        assert 204 == response.status_code

        response = await self.get('/api/v1/topics/1/items/1')
        assert 404 == response.status_code

    async def test_list_items(self):
        response = await self.get('/api/v1/topics/1/items')
        assert 0 == len(self.get_data_from_response(response, 'items'))

        await self._create_item()
        response = await self.get('/api/v1/topics/1/items')
        assert 1 == len(self.get_data_from_response(response, 'items'))

        await self._create_item()
        response = await self.get('/api/v1/topics/1/items')
        assert 2 == len(self.get_data_from_response(response, 'items'))

    async def test_delete_topic_should_delete_item(self, db):
        test_topic = Topic(content='deleted_topic', user_id=1)
        db.add(test_topic)
        await db.commit()
        await db.flush()

        response = await self._create_item(topic_id=test_topic.id)
        assert 201 == response.status_code
        item_id = self.get_data_from_response(response, 'id')

        response = await self.delete(f'/api/v1/topics/{test_topic.id}')
        assert 204 == response.status_code

        item_query = await db.scalars(
            select(Item)
            .where(Item.id == item_id)
            .limit(1)
        )
        assert 0 == len(item_query.all())

    async def test_create_many_items(self):
        await self._create_item()
        await self._create_item(rank=1)
        await self._create_item(rank=2)
        await self._create_item(rank=1)
        await self._create_item(rank=140)

        response = await self.get('/api/v1/topics/1/items')
        assert 200 == response.status_code
        assert 4 == self.get_data_from_response(response, 'items.0.rank')
        assert 2 == self.get_data_from_response(response, 'items.1.rank')
        assert 3 == self.get_data_from_response(response, 'items.2.rank')
        assert 1 == self.get_data_from_response(response, 'items.3.rank')
        assert 5 == self.get_data_from_response(response, 'items.4.rank')

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_item(self, db):
        # creating item as main user
        response = await self._create_item()
        item_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        await self.login(db, self.other_user_id)
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        assert 404 == response.status_code
        assert f'Item {item_id} does not exist' == self.get_data_from_response(response, 'detail')

        # logging back in as main user
        await self.login(db)
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        assert 204 == response.status_code

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_item(self, db):
        # creating item as main user
        response = await self._create_item()
        item_id = self.get_data_from_response(response, 'id')

        # logging in as admin
        await self.login(db, self.other_user_id)
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        assert 204 == response.status_code

    async def test_update_item_belonging_to_another_user(self):
        await self._create_item()
        await self._create_item()
        response = await self._create_item()
        item_to_update_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/1/items/{item_to_update_id}', {
            'content': 'new content',
            'rank': 1
        })
        assert 204 == response.status_code

        response = await self.get(f'/api/v1/topics/1/items/{item_to_update_id}')
        assert 200 == response.status_code
        assert 'new content' == self.get_data_from_response(response, 'item.content')
        assert 1 == self.get_data_from_response(response, 'item.rank')

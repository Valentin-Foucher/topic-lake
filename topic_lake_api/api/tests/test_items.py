import uuid

from sqlalchemy import select, delete

from topic_lake_api.api.tests.base import HttpTestCase
from topic_lake_api.api.tests.decorators import with_another_user
from topic_lake_api.infra.db.core import get_session
from topic_lake_api.infra.db.models import Item, Topic


class ItemsTestCase(HttpTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with get_session() as session:
            session.add(Topic(content='Holiday destinations', user_id=1))
            session.commit()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        with get_session() as session:
            session.execute(
                delete(Item)
            )

    async def _create_item(self, status_code=201, error_message='', topic_id=1, **overriding_dict):
        response = await self.post(f'/api/v1/topics/{topic_id}/items', {
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

    def _assert_item(self, item):
        self.assertIsInstance(item['id'], int)
        self.assertIsInstance(item['content'], str)
        self.assertEqual('test_user', item['user_name'])
        self.assertEqual('Holiday destinations', item['topic_content'])

    async def test_create_with_invalid_content(self):
        await self._create_item(content=111,
                                status_code=422,
                                error_message='Input should be a valid string')
        await self._create_item(content='a' * 2,
                                status_code=422,
                                error_message='String should have at least 3 characters')
        await self._create_item(content='a' * 257,
                                status_code=422,
                                error_message='String should have at most 256 characters')

    async def test_recreate_already_existing_topic(self):
        content = 'already existing item'
        await self._create_item(content=content)
        await self._create_item(content=content,
                                status_code=400,
                                error_message='This item already exists')
        await self._create_item(content=content.upper(),
                                status_code=400,
                                error_message='This item already exists')

    async def test_create_item(self):
        await self._create_item()

    async def test_get_unknown_item(self):
        response = await self.get('/api/v1/topics/1/items/123456')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Item 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_get_item(self):
        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/api/v1/topics/1/items/{inserted_it}')
        self.assertEqual(200, response.status_code)
        self._assert_item(self.get_data_from_response(response, 'item'))

    async def test_delete_item(self):
        response = await self.delete('/api/v1/topics/1/items/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Item 1 does not exist', self.get_data_from_response(response, 'detail'))

        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/api/v1/topics/1/items/{inserted_it}')
        self.assertEqual(204, response.status_code)

        response = await self.get('/api/v1/topics/1/items/1')
        self.assertEqual(404, response.status_code)

    async def test_list_items(self):
        response = await self.get('/api/v1/topics/1/items')
        self.assertEqual(0, len(self.get_data_from_response(response, 'items')))

        await self._create_item()
        response = await self.get('/api/v1/topics/1/items')
        self.assertEqual(1, len(self.get_data_from_response(response, 'items')))

        await self._create_item()
        response = await self.get('/api/v1/topics/1/items')
        self.assertEqual(2, len(self.get_data_from_response(response, 'items')))

    async def test_delete_topic_should_delete_item(self):
        test_topic = Topic(content='deleted_topic', user_id=1)
        with get_session() as session:
            session.add(test_topic)
            session.flush()
            session.commit()

            test_topic_id = test_topic.id

        response = await self._create_item(topic_id=test_topic_id)
        self.assertEqual(201, response.status_code)
        item_id = self.get_data_from_response(response, 'id')

        response = await self.delete(f'/api/v1/topics/{test_topic_id}')
        self.assertEqual(204, response.status_code)

        with get_session() as session:
            item_query = session.scalars(
                select(Item)
                .where(Item.id == item_id)
                .limit(1)
            )
        self.assertEqual(0, len(item_query.all()))

    async def test_create_many_items(self):
        response = await self._create_item()
        first_id = self.get_data_from_response(response, 'id')
        response = await self._create_item(rank=1)
        second_id = self.get_data_from_response(response, 'id')
        response = await self._create_item(rank=2)
        third_id = self.get_data_from_response(response, 'id')
        response = await self._create_item(rank=1)
        fourth_id = self.get_data_from_response(response, 'id')
        response = await self._create_item(rank=140)
        fifth_id = self.get_data_from_response(response, 'id')

        response = await self.get('/api/v1/topics/1/items')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, self.get_data_from_response(response, 'items.0.rank'))
        self.assertEqual(fourth_id, self.get_data_from_response(response, 'items.0.id'))
        self.assertEqual(2, self.get_data_from_response(response, 'items.1.rank'))
        self.assertEqual(second_id, self.get_data_from_response(response, 'items.1.id'))
        self.assertEqual(3, self.get_data_from_response(response, 'items.2.rank'))
        self.assertEqual(third_id, self.get_data_from_response(response, 'items.2.id'))
        self.assertEqual(4, self.get_data_from_response(response, 'items.3.rank'))
        self.assertEqual(first_id, self.get_data_from_response(response, 'items.3.id'))
        self.assertEqual(5, self.get_data_from_response(response, 'items.4.rank'))
        self.assertEqual(fifth_id, self.get_data_from_response(response, 'items.4.id'))

    @with_another_user()
    async def test_user_should_not_be_able_to_delete_another_user_item(self):
        # creating item as main user
        response = await self._create_item()
        item_id = self.get_data_from_response(response, 'id')

        # logging in as another user
        self.login(self.other_user_id)
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        self.assertEqual(404, response.status_code)
        self.assertEqual(f'Item {item_id} does not exist', self.get_data_from_response(response, 'detail'))

        # logging back in as main user
        self.login()
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        self.assertEqual(204, response.status_code)

    @with_another_user(admin=True)
    async def test_admin_should_be_able_to_delete_another_user_item(self):
        # creating item as main user
        response = await self._create_item()
        item_id = self.get_data_from_response(response, 'id')

        # logging in as admin
        self.login(self.other_user_id)
        response = await self.delete(f'/api/v1/topics/1/items/{item_id}')
        self.assertEqual(204, response.status_code)

    async def test_update_item_belonging_to_another_user(self):
        await self._create_item()
        await self._create_item()
        response = await self._create_item()
        item_to_update_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/1/items/{item_to_update_id}', {
            'content': 'new content',
            'rank': 1
        })
        self.assertEqual(204, response.status_code)

        response = await self.get(f'/api/v1/topics/1/items/{item_to_update_id}')
        self.assertEqual(200, response.status_code)
        self.assertEqual('new content', self.get_data_from_response(response, 'item.content'))
        self.assertEqual(1, self.get_data_from_response(response, 'item.rank'))

    async def test_update_topic_but_a_similar_one_already_exists(self):
        content = 'already existing item'
        await self._create_item(content=content)

        response = await self._create_item()
        item_to_update_id = self.get_data_from_response(response, 'id')

        response = await self.put(f'/api/v1/topics/1/items/{item_to_update_id}', {
            'content': 'already existing item',
            'rank': 1
        })
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            'Cannot rename this item, a similar item already exists',
            self.get_data_from_response(response, 'detail')
        )

from sqlalchemy import select

from topic_recommendations.api.tests.base import HttpTestCase
from topic_recommendations.infra.db.core import session
from topic_recommendations.infra.db.models import Item, Topic


class ItemsTestCase(HttpTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        session.add(Topic(content='Holiday destinations', user_id=1))
        session.commit()

    async def asyncSetUp(self):
        await super().asyncSetUp()
        Item.query.delete()

    async def _create_item(self, status_code=201, error_message='', topic_id=1, **overriding_dict):
        response = await self.post(f'/topics/{topic_id}/items', {
            'content': 'Ibiza',
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

    def _assert_item(self, item):
        self.assertIsInstance(item['id'], int)
        self.assertEqual('Ibiza', item['content'])
        self.assertEqual('test_user', item['user_name'])
        self.assertEqual('Holiday destinations', item['topic_content'])

    async def test_create_with_invalid_content(self):
        await self._create_item(content=111,
                                status_code=422,
                                error_message='Input should be a valid string')

    async def test_create_with_invalid_user_id(self):
        await self._create_item(user_id='not a valid id',
                                status_code=422,
                                error_message='Input should be a valid integer, unable to parse string as an integer')
        await self._create_item(user_id=13,
                                status_code=404,
                                error_message='User 13 does not exist')

    async def test_create_item(self):
        await self._create_item()

    async def test_get_unknown_item(self):
        response = await self.get('/topics/1/items/123456')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Item 123456 does not exist', self.get_data_from_response(response, 'detail'))

    async def test_get_item(self):
        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')

        response = await self.get(f'/topics/1/items/{inserted_it}')
        self.assertEqual(200, response.status_code)
        self._assert_item(self.get_data_from_response(response, 'item'))

    async def test_delete_item(self):
        response = await self.delete('/topics/1/items/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual('Item 1 does not exist', self.get_data_from_response(response, 'detail'))

        response = await self._create_item()
        inserted_it = self.get_data_from_response(response, 'id')
        response = await self.delete(f'/topics/1/items/{inserted_it}')
        self.assertEqual(204, response.status_code)

        response = await self.get('/topics/1/items/1')
        self.assertEqual(404, response.status_code)

    async def test_list_items(self):
        response = await self.get('/topics/1/items')
        self.assertEqual(0, len(self.get_data_from_response(response, 'items')))

        await self._create_item()
        response = await self.get('/topics/1/items')
        self.assertEqual(1, len(self.get_data_from_response(response, 'items')))

        await self._create_item()
        response = await self.get('/topics/1/items')
        self.assertEqual(2, len(self.get_data_from_response(response, 'items')))

    async def test_delete_topic_should_delete_item(self):
        test_topic = Topic(content='deleted_topic', user_id=1)
        session.add(test_topic)
        session.commit()
        session.flush()

        response = await self._create_item(topic_id=test_topic.id)
        self.assertEqual(201, response.status_code)
        item_id = self.get_data_from_response(response, 'id')

        response = await self.delete(f'/topics/{test_topic.id}')
        self.assertEqual(204, response.status_code)

        item_query = session.scalars(
            select(Item)
            .where(Item.id == item_id)
            .limit(1)
        )
        self.assertEqual(0, len(item_query.all()))

from django.test import TestCase, Client
from artifact_recommender.models import Dataset, BuildingBlock, Tag
from django.contrib.auth.models import User
import base64
import json
# Create your tests here.

BASIC_USER = 'test-user'
BASIC_PASSWORD = 'test-password'


class BuildingBlockTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        self.client = Client()

    def test_create_buildingblock_anon(self):
        response = self.client.post('/buildingblock/',
                                    json.dumps({'id': 4444,
                                                'lang': 'spanish',
                                                'tags': ['tag1', 'tag2']}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(BuildingBlock.objects.count(), 0)

    def test_create_buildingblock(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

    def test_update_buildingblock_anon(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.put(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        building_block = BuildingBlock.objects.first()
        self.assertEqual(building_block.lang, 'spanish')
        tags = []
        for tag in building_block.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag1', 'tag2'])

    def test_update_buildingblock(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.put(
            '/buildingblock/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 200)

        building_block = BuildingBlock.objects.first()
        self.assertEqual(building_block.lang, 'italian')
        tags = []
        for tag in building_block.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag3', 'tag4'])

    def test_delete_buildingblock_anon(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.delete('/buildingblock/4444/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(BuildingBlock.objects.count(), 1)

    def test_delete_buildingblock(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.delete(
            '/buildingblock/4444/',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(BuildingBlock.objects.count(), 0)

    def test_get_buildingblocks(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.get('/buildingblock/')

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

    def test_get_buildingblock(self):
        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 1)

        response = self.client.get('/buildingblock/4444/')

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], 4444)
        self.assertEqual(response_json['lang'], 'spanish')
        self.assertListEqual(response_json['tags'], ['tag1', 'tag2'])


class DatasetTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        self.client = Client()

    def test_create_dataset_anon(self):
        response = self.client.post('/dataset/',
                                    json.dumps({'id': 4444,
                                                'lang': 'spanish',
                                                'tags': ['tag1', 'tag2']}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Dataset.objects.count(), 0)

    def test_create_dataset(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

    def test_update_dataset_anon(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.put(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        dataset = Dataset.objects.first()
        self.assertEqual(dataset.lang, 'spanish')
        tags = []
        for tag in dataset.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag1', 'tag2'])

    def test_update_dataset(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.put(
            '/dataset/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 200)

        dataset = Dataset.objects.first()
        self.assertEqual(dataset.lang, 'italian')
        tags = []
        for tag in dataset.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag3', 'tag4'])

    def test_delete_dataset_anon(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.delete('/dataset/4444/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Dataset.objects.count(), 1)

    def test_delete_dataset(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.delete(
            '/dataset/4444/',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Dataset.objects.count(), 0)

    def test_get_dataset(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.get('/dataset/')

        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

    def test_get_dataset(self):
        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 1)

        response = self.client.get('/dataset/4444/')

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], 4444)
        self.assertEqual(response_json['lang'], 'spanish')
        self.assertListEqual(response_json['tags'], ['tag1', 'tag2'])

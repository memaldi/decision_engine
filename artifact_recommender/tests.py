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


class DatasetTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')

    def test_create_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        dataset = Dataset.objects.create(id=4444, lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), three_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(dataset.id, 4444)
        self.assertEqual(Dataset.objects.count(), 1)

        two_tag_list = [self.tag1, self.tag2]
        dataset = Dataset.objects.create(id=5555, lang='spanish')
        dataset.tags = two_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), two_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(dataset.id, 5555)
        self.assertEqual(Dataset.objects.count(), 2)

    def test_update_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        two_tag_list = [self.tag1, self.tag2]
        dataset = Dataset.objects.create(id=4444, lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), three_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(dataset.id, 4444)
        self.assertEqual(Dataset.objects.count(), 1)

        dataset.lang = 'italian'
        dataset.tags = two_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), two_tag_list)
        self.assertEqual(dataset.lang, 'italian')
        self.assertEqual(dataset.id, 4444)
        self.assertEqual(Dataset.objects.count(), 1)

    def test_delete_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        dataset = Dataset.objects.create(id=4444, lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        self.assertEqual(Dataset.objects.count(), 1)

        dataset = Dataset.objects.last()
        dataset.delete()

        self.assertEqual(Dataset.objects.count(), 0)

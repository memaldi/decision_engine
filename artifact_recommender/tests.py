from django.test import TestCase, Client
from artifact_recommender.models import Dataset, BuildingBlock, Tag
from artifact_recommender.models import Application, Idea
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
            '/buildingblock/4444/',
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

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

        response = self.client.post(
            '/buildingblock/',
            json.dumps({'id': 4445,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BuildingBlock.objects.count(), 2)

        response = self.client.get('/buildingblock/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

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
            '/dataset/4444/',
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

    def test_get_datasets(self):
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

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

        response = self.client.post(
            '/dataset/',
            json.dumps({'id': 4445,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Dataset.objects.count(), 2)

        response = self.client.get('/dataset/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

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


class ApplicationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        self.client = Client()

    def test_create_app_anon(self):
        response = self.client.post('/app/',
                                    json.dumps({'id': 4444,
                                                'lang': 'spanish',
                                                'tags': ['tag1', 'tag2'],
                                                'scope': 'Bilbao',
                                                'min_age': 13}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Application.objects.count(), 0)

    def test_create_app(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

    def test_update_app_anon(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.put(
            '/app/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4'],
                        'scope': 'Trento',
                        'min_age': 15}),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        app = Application.objects.first()
        self.assertEqual(app.lang, 'spanish')
        self.assertEqual(app.scope, 'Bilbao')
        self.assertEqual(app.min_age, 13)

        tags = []
        for tag in app.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag1', 'tag2'])

    def test_update_app(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.put(
            '/app/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4'],
                        'scope': 'Trento',
                        'min_age': 15}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 200)

        app = Application.objects.first()
        self.assertEqual(app.lang, 'italian')
        tags = []
        for tag in app.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag3', 'tag4'])

    def test_delete_app_anon(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.delete('/app/4444/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Application.objects.count(), 1)

    def test_delete_app(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.delete(
            '/app/4444/',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Application.objects.count(), 0)

    def test_get_apps(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.get('/app/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

        response = self.client.post(
            '/app/',
            json.dumps({'id': 4445,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 2)

        response = self.client.get('/app/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

    def test_get_app(self):
        response = self.client.post(
            '/app/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2'],
                        'scope': 'Bilbao',
                        'min_age': 13}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Application.objects.count(), 1)

        response = self.client.get('/app/4444/')

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], 4444)
        self.assertEqual(response_json['lang'], 'spanish')
        self.assertListEqual(response_json['tags'], ['tag1', 'tag2'])
        self.assertEqual(response_json['scope'], 'Bilbao')
        self.assertEqual(response_json['min_age'], 13)


class IdeaTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(BASIC_USER, password=BASIC_PASSWORD)
        user.save()

        self.client = Client()

    def test_create_idea_anon(self):
        response = self.client.post('/idea/',
                                    json.dumps({'id': 4444,
                                                'lang': 'spanish',
                                                'tags': ['tag1', 'tag2']}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Idea.objects.count(), 0)

    def test_create_idea(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

    def test_update_idea_anon(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.put(
            '/idea/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)

        idea = Idea.objects.first()
        self.assertEqual(idea.lang, 'spanish')
        tags = []
        for tag in idea.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag1', 'tag2'])

    def test_update_idea(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.put(
            '/idea/4444/',
            json.dumps({'id': 4444,
                        'lang': 'italian',
                        'tags': ['tag3', 'tag4']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 200)

        idea = Idea.objects.first()
        self.assertEqual(idea.lang, 'italian')
        tags = []
        for tag in idea.tags.all():
            tags.append(tag.name)
        self.assertListEqual(tags, ['tag3', 'tag4'])

    def test_delete_idea_anon(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.delete('/idea/4444/')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(Idea.objects.count(), 1)

    def test_delete_idea(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.delete(
            '/idea/4444/',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Idea.objects.count(), 0)

    def test_get_ideas(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.get('/idea/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 1)

        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4445,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 2)

        response = self.client.get('/idea/')

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertEqual(len(response_json), 2)

    def test_get_idea(self):
        response = self.client.post(
            '/idea/',
            json.dumps({'id': 4444,
                        'lang': 'spanish',
                        'tags': ['tag1', 'tag2']}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'BASIC {}'.format(
                base64.b64encode('{}:{}'.format(
                     BASIC_USER, BASIC_PASSWORD).encode()).decode())},
            follow=True)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Idea.objects.count(), 1)

        response = self.client.get('/idea/4444/')

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.content)
        self.assertEqual(response_json['id'], 4444)
        self.assertEqual(response_json['lang'], 'spanish')
        self.assertListEqual(response_json['tags'], ['tag1', 'tag2'])

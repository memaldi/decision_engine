from django.test import TestCase
from artifact_recommender.models import Dataset, BuildingBlock, Application
from artifact_recommender.models import Idea, Similarity, Tag
# Create your tests here.


class BuildingBlockTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')

    def test_create_buildingblock(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        building_block = BuildingBlock.objects.create(lang='spanish')
        building_block.tags = three_tag_list
        building_block.save()

        building_block = BuildingBlock.objects.last()

        self.assertListEqual(list(building_block.tags.all()), three_tag_list)
        self.assertEqual(building_block.lang, 'spanish')
        self.assertEqual(BuildingBlock.objects.count(), 1)

        two_tag_list = [self.tag1, self.tag2]
        building_block = BuildingBlock.objects.create(lang='spanish')
        building_block.tags = two_tag_list
        building_block.save()

        building_block = BuildingBlock.objects.last()

        self.assertListEqual(list(building_block.tags.all()), two_tag_list)
        self.assertEqual(building_block.lang, 'spanish')
        self.assertEqual(BuildingBlock.objects.count(), 2)

    def test_update_buildingblock(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        two_tag_list = [self.tag1, self.tag2]
        building_block = BuildingBlock.objects.create(lang='spanish')
        building_block.tags = three_tag_list
        building_block.save()

        building_block = BuildingBlock.objects.last()

        self.assertListEqual(list(building_block.tags.all()), three_tag_list)
        self.assertEqual(building_block.lang, 'spanish')
        self.assertEqual(BuildingBlock.objects.count(), 1)

        building_block.lang = 'italian'
        building_block.tags = two_tag_list
        building_block.save()

        building_block = BuildingBlock.objects.last()

        self.assertListEqual(list(building_block.tags.all()), two_tag_list)
        self.assertEqual(building_block.lang, 'italian')
        self.assertEqual(BuildingBlock.objects.count(), 1)

    def test_delete_buildingblock(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        building_block = BuildingBlock.objects.create(lang='spanish')
        building_block.tags = three_tag_list
        building_block.save()

        self.assertEqual(BuildingBlock.objects.count(), 1)

        building_block = BuildingBlock.objects.last()
        building_block.delete()

        self.assertEqual(BuildingBlock.objects.count(), 0)


class DatasetTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')
        self.tag3 = Tag.objects.create(name='tag3')

    def test_create_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        dataset = Dataset.objects.create(lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), three_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(Dataset.objects.count(), 1)

        two_tag_list = [self.tag1, self.tag2]
        dataset = Dataset.objects.create(lang='spanish')
        dataset.tags = two_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), two_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(Dataset.objects.count(), 2)

    def test_update_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        two_tag_list = [self.tag1, self.tag2]
        dataset = Dataset.objects.create(lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), three_tag_list)
        self.assertEqual(dataset.lang, 'spanish')
        self.assertEqual(Dataset.objects.count(), 1)

        dataset.lang = 'italian'
        dataset.tags = two_tag_list
        dataset.save()

        dataset = Dataset.objects.last()

        self.assertListEqual(list(dataset.tags.all()), two_tag_list)
        self.assertEqual(dataset.lang, 'italian')
        self.assertEqual(Dataset.objects.count(), 1)

    def test_delete_dataset(self):
        three_tag_list = [self.tag1, self.tag2, self.tag3]
        dataset = Dataset.objects.create(lang='spanish')
        dataset.tags = three_tag_list
        dataset.save()

        self.assertEqual(Dataset.objects.count(), 1)

        dataset = Dataset.objects.last()
        dataset.delete()

        self.assertEqual(Dataset.objects.count(), 0)

from drb.topics.dao import ManagerDao
import unittest
import uuid
import os
import drb.topics.resolver as resolver


class TestGeoJson(unittest.TestCase):
    def test_topic(self):
        topic_id = 'd8c867e8-7185-4a82-adbe-a5f2a5ef63b6'
        topic = ManagerDao().get_drb_topic(uuid.UUID(topic_id))
        self.assertIsNotNone(topic)
        self.assertEqual('GeoJSON', topic.label)
        self.assertEqual('json', topic.factory)

    def test_resolver(self):
        directory = os.path.join(os.path.dirname(__file__), 'resources')

        path = os.path.join(directory, 'no_geojson_data.json')
        topic, node = resolver.resolve(path)
        self.assertNotEqual(topic.label, 'GeoJSON')

        path = os.path.join(directory, 'french_region.json')
        topic, node = resolver.resolve(path)
        self.assertEqual(topic.label, 'GeoJSON')

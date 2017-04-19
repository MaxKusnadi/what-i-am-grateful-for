import unittest
import app


class TestGratitudeView(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_get(self):
        result = self.app.get('/')

        assert b'YOUR GRATITUDE' in result.data


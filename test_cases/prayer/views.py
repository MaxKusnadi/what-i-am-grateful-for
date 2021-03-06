import unittest
import app


class TestPrayerView(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_get(self):
        result = self.app.get('/prayer')

        assert b'Here is my prayer intention...' in result.data

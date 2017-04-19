import unittest
import app
import tempfile
import os

from app.gratitude.controller import GratitudeController


class TestGratitudeController(unittest.TestCase):

    def setUp(self):
        self.controller = GratitudeController()
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        app.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_add_gratitude_success(self):
        message = {
            "data": "HELLO"
        }
        gratitude = self.controller.on_add_gratitude(message)

        assert gratitude.message == message['data']

    def test_add_gratitude_failure(self):
        message = {
            "data": " "
        }
        gratitude = self.controller.on_add_gratitude(message)

        assert gratitude is None

    def test_get_all_gratitudes(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        gratitude_1 = self.controller.on_add_gratitude(message_1)
        gratitude_2 = self.controller.on_add_gratitude(message_2)

        all_gratitudes = self.controller.get_all_gratitudes()

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes

    def test_delete_gratitude(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        gratitude_1 = self.controller.on_add_gratitude(message_1)
        gratitude_2 = self.controller.on_add_gratitude(message_2)

        all_gratitudes = self.controller.get_all_gratitudes()

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes

        self.controller.delete_gratitude(gratitude_1.id)

        all_gratitudes_after = self.controller.get_all_gratitudes()

        assert gratitude_1 not in all_gratitudes_after
        assert gratitude_2 in all_gratitudes_after

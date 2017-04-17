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
        message = "HELLO"
        gratitude = self.controller.add_gratitude(message)

        assert gratitude.message == message

    def test_add_gratitude_failure(self):
        message = ""
        self.assertRaises(ValueError, self.controller.add_gratitude, message)

    def test_get_all_gratitudes(self):
        gratitude_1 = self.controller.add_gratitude("HELLO 1")
        gratitude_2 = self.controller.add_gratitude("HELLO 2")

        all_gratitudes = self.controller.get_all_gratitudes()

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes

    def test_delete_gratitude(self):
        gratitude_1 = self.controller.add_gratitude("HELLO 1")
        gratitude_2 = self.controller.add_gratitude("HELLO 2")

        all_gratitudes = self.controller.get_all_gratitudes()

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes

        self.controller.delete_gratitude(gratitude_1.id)

        all_gratitudes_after = self.controller.get_all_gratitudes()

        assert gratitude_1 not in all_gratitudes_after
        assert gratitude_2 in all_gratitudes_after

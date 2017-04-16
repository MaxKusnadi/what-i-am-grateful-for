import os
import unittest
import tempfile
import app

from datetime import datetime
from app.gratitude.models import Gratitude, GratitudeDatabaseController


class TestGratitudeModel(unittest.TestCase):

    def test_model(self):
        now = datetime.now()
        time = now.isoformat()
        message = "HELLO"
        g = Gratitude(message, time)

        assert g.message == message
        assert g.datetime == time


class TestGratitudeDatabaseController(unittest.TestCase):

    def setUp(self):
        self.controller = GratitudeDatabaseController()
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        app.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_add_gratitude(self):
        message = "Hello world"
        now = datetime.now()
        now = now.isoformat()
        gratitude = self.controller.add_gratitude(message, now)
        gratitude_id = gratitude.id

        g = Gratitude.query.filter(Gratitude.id == gratitude_id).first()

        assert g.message == message
        assert g.datetime == now

    def test_delete_gratitude(self):
        message = "test"
        now = datetime.now()
        now = now.isoformat()
        gratitude = self.controller.add_gratitude(message, now)
        gratitude_id = gratitude.id
        all_gratitudes_before = Gratitude.query.all()
        assert gratitude in all_gratitudes_before

        self.controller.delete_gratitude(gratitude_id)

        all_gratitudes_after = Gratitude.query.all()
        self.assertFalse(gratitude in all_gratitudes_after)

    def test_get_all_gratitudes(self):
        message_1 = "test"
        time_1 = datetime.strptime("30/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_1 = self.controller.add_gratitude(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("30/Nov/00 18:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_2 = self.controller.add_gratitude(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("30/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_3 = Gratitude(message_3, time_3)

        all_gratitudes = self.controller.get_gratitudes()

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes
        assert gratitude_3 not in all_gratitudes

    def test_get_specific_gratitudes(self):
        message_1 = "test"
        time_1 = datetime.strptime("15/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_1 = self.controller.add_gratitude(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("20/Nov/00 18:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_2 = self.controller.add_gratitude(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("30/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        gratitude_3 = self.controller.add_gratitude(message_3, time_3)

        start_date = datetime.strptime("10/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        end_date = datetime.strptime("25/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()

        all_gratitudes = self.controller.get_gratitudes(start_date=start_date,
                                                        end_date=end_date)

        assert gratitude_1 in all_gratitudes
        assert gratitude_2 in all_gratitudes
        assert  gratitude_3 not in all_gratitudes

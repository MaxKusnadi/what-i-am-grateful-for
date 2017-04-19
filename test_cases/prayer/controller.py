import unittest
import app
import tempfile
import os

from app.prayer.controller import PrayerController


class TestPrayerController(unittest.TestCase):

    def setUp(self):
        self.controller = PrayerController()
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        app.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_add_prayer_success(self):
        message = {
            "data": "HELLO"
        }
        prayer = self.controller.on_add_prayer(message)

        assert prayer.message == message['data']

    def test_add_prayer_failure(self):
        message = {
            "data": ""
        }
        self.assertRaises(ValueError, self.controller.on_add_prayer, message)

    def test_pray_prayer(self):
        message = {
            "data": "HELLO"
        }

        prayer_before = self.controller.on_add_prayer(message)
        assert prayer_before.isPrayed is False

        prayer_after = self.controller.pray_prayer(prayer_before.id)
        assert prayer_after.isPrayed is True

    def test_get_all_unprayed_prayers(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        prayer_1 = self.controller.on_add_prayer(message_1)
        prayer_2 = self.controller.on_add_prayer(message_2)

        all_unprayed_prayers = self.controller.get_unprayed_prayers()
        all_prayed_prayers = self.controller.get_prayed_prayers()

        assert prayer_1 in all_unprayed_prayers
        assert prayer_2 in all_unprayed_prayers
        assert prayer_1 not in all_prayed_prayers
        assert prayer_2 not in all_prayed_prayers

    def test_get_all_prayed_prayers(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        prayer_1 = self.controller.on_add_prayer(message_1)
        prayer_2 = self.controller.on_add_prayer(message_2)

        prayer_1 = self.controller.pray_prayer(prayer_1.id)
        prayer_2 = self.controller.pray_prayer(prayer_2.id)

        all_unprayed_prayers = self.controller.get_unprayed_prayers()
        all_prayed_prayers = self.controller.get_prayed_prayers()

        assert prayer_1 not in all_unprayed_prayers
        assert prayer_2 not in all_unprayed_prayers
        assert prayer_1 in all_prayed_prayers
        assert prayer_2 in all_prayed_prayers

    def test_delete_unprayed_prayer(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        prayer_1 = self.controller.on_add_prayer(message_1)
        prayer_2 = self.controller.on_add_prayer(message_2)

        all_unprayed_prayers = self.controller.get_unprayed_prayers()

        assert prayer_1 in all_unprayed_prayers
        assert prayer_2 in all_unprayed_prayers

        self.controller.delete_prayer(prayer_1.id)

        all_unprayed_prayers_after = self.controller.get_unprayed_prayers()

        assert prayer_1 not in all_unprayed_prayers_after
        assert prayer_2 in all_unprayed_prayers_after

    def test_delete_prayed_prayer(self):
        message_1 = {
            "data": "HELLO 1"
        }
        message_2 = {
            "data": "HELLO 2"
        }
        prayer_1 = self.controller.on_add_prayer(message_1)
        prayer_2 = self.controller.on_add_prayer(message_2)

        prayer_1 = self.controller.pray_prayer(prayer_1.id)
        prayer_2 = self.controller.pray_prayer(prayer_2.id)

        all_prayed_prayers = self.controller.get_prayed_prayers()

        assert prayer_1 in all_prayed_prayers
        assert prayer_2 in all_prayed_prayers

        self.controller.delete_prayer(prayer_1.id)

        all_prayed_prayers_after = self.controller.get_prayed_prayers()

        assert prayer_1 not in all_prayed_prayers_after
        assert prayer_2 in all_prayed_prayers_after

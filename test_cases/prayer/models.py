import unittest
import tempfile
import os
import app

from datetime import datetime
from app.prayer.models import Prayer, PrayerDatabaseController


class TestPrayerModel(unittest.TestCase):

    def test_model(self):
        now = datetime.now()
        time = now.isoformat()
        message = "HELLO"
        g = Prayer(message, time)

        assert g.message == message
        assert g.datetime == time
        self.assertFalse(g.isPrayed)

        g.prayed()

        self.assertTrue(g.isPrayed)


class TestPrayerDatabaseController(unittest.TestCase):

    def setUp(self):
        self.controller = PrayerDatabaseController()
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        app.db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_add_prayer(self):
        message = "Hello world"
        now = datetime.now()
        now = now.isoformat()
        prayer = self.controller.add_prayer(message, now)
        prayer_id = prayer.id

        p = Prayer.query.filter(Prayer.id == prayer_id).first()

        assert p.message == message
        assert p.datetime == now
        assert p.isPrayed is False

    def test_delete_prayer(self):
        message = "test"
        now = datetime.now()
        now = now.isoformat()
        prayer = self.controller.add_prayer(message, now)
        prayer_id = prayer.id
        all_prayer_before = Prayer.query.all()
        assert prayer in all_prayer_before

        self.controller.delete_prayer(prayer_id)

        all_prayer_after = Prayer.query.all()
        self.assertFalse(prayer in all_prayer_after)

    def test_pray_prayer(self):
        message = "test"
        now = datetime.now()
        now = now.isoformat()
        prayer = self.controller.add_prayer(message, now)
        prayer_id = prayer.id
        assert not prayer.isPrayed

        self.controller.pray_prayer(prayer_id)

        assert prayer.isPrayed

    def test_get_all_unprayed_prayers(self):

        message_1 = "test"
        time_1 = datetime.strptime("30/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_1 = self.controller.add_prayer(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("29/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_2 = self.controller.add_prayer(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("3/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_3 = Prayer(message_3, time_3)

        message_4 = "test 4"
        time_4 = datetime.strptime("23/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_4 = self.controller.add_prayer(message_4, time_4)

        self.controller.pray_prayer(pray_4.id)

        message_5 = "test 5"
        time_5 = datetime.strptime("13/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_5 = self.controller.add_prayer(message_5, time_5)

        self.controller.pray_prayer(pray_5.id)

        all_unprayed_prayers_after = self.controller.get_unprayed_prayers()

        assert pray_1 in all_unprayed_prayers_after
        assert pray_2 in all_unprayed_prayers_after
        assert pray_3 not in all_unprayed_prayers_after
        assert pray_4 not in all_unprayed_prayers_after
        assert pray_5 not in all_unprayed_prayers_after


    def test_get_specific_unprayed_prayers(self):
        message_1 = "test"
        time_1 = datetime.strptime("1/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        pray_1 = self.controller.add_prayer(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("17/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_2 = self.controller.add_prayer(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("15/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_3 = self.controller.add_prayer(message_3, time_3)

        message_4 = "test 4"
        time_4 = datetime.strptime("10/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_4 = self.controller.add_prayer(message_4, time_4)

        self.controller.pray_prayer(pray_4.id)

        message_5 = "test 5"
        time_5 = datetime.strptime("23/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_5 = self.controller.add_prayer(message_5, time_5)

        self.controller.pray_prayer(pray_5.id)

        message_6 = "test 6"
        time_6 = datetime.strptime("20/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_6 = self.controller.add_prayer(message_6, time_6)

        start_date = datetime.strptime("1/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        end_date = datetime.strptime("17/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()

        all_unprayed_prayers = self.controller.get_unprayed_prayers(start_date=start_date,
                                                                    end_date=end_date)

        assert pray_1 in all_unprayed_prayers
        assert pray_2 in all_unprayed_prayers
        assert pray_3 in all_unprayed_prayers
        assert pray_4 not in all_unprayed_prayers
        assert pray_5 not in all_unprayed_prayers
        assert pray_6 not in all_unprayed_prayers

    def test_get_all_prayed_prayers(self):
        message_1 = "test"
        time_1 = datetime.strptime("30/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_1 = self.controller.add_prayer(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("29/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_2 = self.controller.add_prayer(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("3/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_3 = Prayer(message_3, time_3)

        message_4 = "test 4"
        time_4 = datetime.strptime("23/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_4 = self.controller.add_prayer(message_4, time_4)

        self.controller.pray_prayer(pray_4.id)

        message_5 = "test 5"
        time_5 = datetime.strptime("13/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_5 = self.controller.add_prayer(message_5, time_5)

        self.controller.pray_prayer(pray_5.id)

        all_prayed_prayers = self.controller.get_prayed_prayers()

        assert pray_1 not in all_prayed_prayers
        assert pray_2 not in all_prayed_prayers
        assert pray_3 not in all_prayed_prayers
        assert pray_4 in all_prayed_prayers
        assert pray_5 in all_prayed_prayers

    def test_get_specific_prayed_prayers(self):
        message_1 = "test"
        time_1 = datetime.strptime("15/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_1 = self.controller.add_prayer(message_1, time_1)

        message_2 = "test 2"
        time_2 = datetime.strptime("9/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_2 = self.controller.add_prayer(message_2, time_2)

        message_3 = "test 3"
        time_3 = datetime.strptime("14/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_3 = self.controller.add_prayer(message_3, time_3)

        self.controller.pray_prayer(pray_3.id)

        message_4 = "test 4"
        time_4 = datetime.strptime("20/Nov/00 20:00", "%d/%b/%y %H:%M").isoformat()
        pray_4 = self.controller.add_prayer(message_4, time_4)

        self.controller.pray_prayer(pray_4.id)

        message_5 = "test 5"
        time_5 = datetime.strptime("23/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_5 = self.controller.add_prayer(message_5, time_5)

        self.controller.pray_prayer(pray_5.id)

        message_6 = "test 6"
        time_6 = datetime.strptime("27/Nov/00 17:00", "%d/%b/%y %H:%M").isoformat()
        pray_6 = self.controller.add_prayer(message_6, time_6)

        self.controller.pray_prayer(pray_6.id)

        start_date = datetime.strptime("20/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()
        end_date = datetime.strptime("27/Nov/00 19:00", "%d/%b/%y %H:%M").isoformat()

        all_prayed_prayers = self.controller.get_prayed_prayers(start_date=start_date,
                                                                end_date=end_date)

        assert pray_1 not in all_prayed_prayers
        assert pray_2 not in all_prayed_prayers
        assert pray_3 not in all_prayed_prayers
        assert pray_4 in all_prayed_prayers
        assert pray_5 in all_prayed_prayers
        assert pray_6 in all_prayed_prayers

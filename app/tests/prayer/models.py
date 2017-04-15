import unittest

from datetime import datetime
from app.prayer.models import Prayer


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

import unittest

from datetime import datetime
from app.gratitude.models import Gratitude


class TestGratitudeModel(unittest.TestCase):

    def test_model(self):
        now = datetime.now()
        time = now.isoformat()
        message = "HELLO"
        g = Gratitude(message, time)

        assert g.message == message
        assert g.datetime == time

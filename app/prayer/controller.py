import logging
import pytz

from datetime import datetime, timedelta
from flask_socketio import Namespace, emit

from app import socketio
from app.prayer.models import PrayerDatabaseController


class PrayerController(Namespace):

    def __init__(self, *args):
        super().__init__(*args)
        self.controller = PrayerDatabaseController()

    def on_add_prayer(self, message):
        message = message['data']
        if not message:
            logging.error("Empty prayer message")
            raise ValueError("Empty message")
        logging.info("Adding a prayer from controller...")
        time = self._get_current_time().isoformat()
        prayer = self.controller.add_prayer(message, time)

        try:
            emit('my_response', {
                 'message': prayer.message,
                 'datetime': time,
                 'isPrayed': prayer.isPrayed
            }, broadcast=True)
        except RuntimeError:
            pass  # for testing purposes

        return prayer

    def delete_prayer(self, id):
        logging.info("Deleting a prayer from controller")
        prayer = self.controller.delete_prayer(id)
        return prayer

    def pray_prayer(self, id):
        logging.info("Praying for a prayer from controller")
        prayer = self.controller.pray_prayer(id)
        return prayer

    def get_prayed_prayers(self):
        logging.info("Getting all prayed prayers from controller")
        now = self._get_current_time()
        start_time = now - timedelta(days=3)

        now = now.isoformat()
        start_time = start_time.isoformat()

        all_prayers = self.controller.get_prayed_prayers(
            start_date=start_time, end_date=now)

        return all_prayers

    def get_unprayed_prayers(self):
        logging.info("Getting all unprayed prayers from controller")
        now = self._get_current_time()
        start_time = now - timedelta(days=3)

        now = now.isoformat()
        start_time = start_time.isoformat()

        all_prayers = self.controller.get_unprayed_prayers(
            start_date=start_time, end_date=now)

        return all_prayers

    def _get_current_time(self): # pragma: no cover
        timezone = pytz.timezone('Asia/Singapore')
        date_now = datetime.now(timezone)
        return date_now

    def on_my_event(self, message): # pragma: no cover
        if message['data']:
            logging.info("A client is connected to the prayer page")

socketio.on_namespace(PrayerController('/prayer'))

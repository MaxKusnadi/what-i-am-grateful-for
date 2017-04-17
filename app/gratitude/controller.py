import logging
import pytz

from datetime import datetime, timedelta
from flask_socketio import Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from app import socketio
from app.gratitude.models import GratitudeDatabaseController


class GratitudeController(Namespace):

    def __init__(self, *args):
        super().__init__(*args)
        self.controller = GratitudeDatabaseController()

    def on_add_gratitude(self, message):
        message = message['data']
        if not message:
            logging.error("Empty gratitude message")
            raise ValueError("Empty message")
        logging.info("Adding a gratitude from controller...")
        time = self._get_current_time().isoformat()
        gratitude = self.controller.add_gratitude(message, time)
        emit('my_response', {
            'message': gratitude.message,
            'datetime': time
        }, broadcast=True)
        return gratitude

    def delete_gratitude(self, id):
        logging.info("Deleting a gratitude from controller")
        gratitude = self.controller.delete_gratitude(id)
        return gratitude

    def get_all_gratitudes(self):
        logging.info("Getting all gratitudes from controller")
        now = self._get_current_time()
        start_time = now - timedelta(days=3)

        now = now.isoformat()
        start_time = start_time.isoformat()

        all_gratitudes = self.controller.get_gratitudes(
            start_date=start_time, end_date=now)

        return all_gratitudes

    def _get_current_time(self): # pragma: no cover
        timezone = pytz.timezone('Asia/Singapore')
        date_now = datetime.now(timezone)
        return date_now

    def on_my_event(self, message): # pragma: no cover
        if message['data']:
            logging.info("Connected")

socketio.on_namespace(GratitudeController('/gratitude'))

import logging
import pytz
import dateutil.parser

from datetime import datetime, timedelta
from flask_socketio import Namespace, emit

from app import socketio
from app.gratitude.models import GratitudeDatabaseController


class GratitudeController(Namespace):

    def __init__(self, *args):
        super().__init__(*args)
        self.controller = GratitudeDatabaseController()

    def on_add_gratitude(self, message):
        message = message['data']
        if not message.strip():
            logging.error("Empty gratitude message")
            return None
        logging.info("Adding a gratitude from controller...")
        time = self._get_current_time()
        time_iso = time.isoformat()
        gratitude = self.controller.add_gratitude(message, time_iso)

        try:
            emit('my_response', {
                 'message': gratitude.message,
                 'datetime': time.strftime("%d/%m/%Y - %H:%M")
            }, broadcast=True)
        except RuntimeError:
            pass  # for testing purposes

        return gratitude

    def delete_gratitude(self, id):
        logging.info("Deleting a gratitude from controller")
        gratitude = self.controller.delete_gratitude(id)
        return gratitude

    def get_all_gratitudes(self):
        logging.info("Getting all gratitudes from controller")
        now = self._get_current_time()
        start_time = now - timedelta(days=365)

        now = now.isoformat()
        start_time = start_time.isoformat()

        all_gratitudes = self.controller.get_gratitudes(
            start_date=start_time, end_date=now)

        all_gratitudes = list(map(lambda x: self._format_date(x), all_gratitudes))

        return all_gratitudes

    def get_all_gratitudes_api(self):
        gratitudes = self.get_all_gratitudes()
        result = list(map(lambda x: {"message": x.message, "datetime": x.datetime}, gratitudes))
        return result

    def _format_date(self, data):
        data.datetime = dateutil.parser.parse(data.datetime).strftime("%d/%m/%Y - %H:%M")
        return data

    def _get_current_time(self): # pragma: no cover
        timezone = pytz.timezone('Asia/Singapore')
        date_now = datetime.now(timezone)
        return date_now

    def on_my_event(self, message): # pragma: no cover
        if message['data']:
            logging.info("A client is connected to the gratitude page")


socketio.on_namespace(GratitudeController('/gratitude'))

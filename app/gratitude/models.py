import logging

from app import db
from sqlalchemy import Column, String, Integer, Text


class Gratitude(db.Model):
    __tablename__ = 'gratitude'

    id = Column(Integer, primary_key=True)
    message = Column(Text)
    datetime = Column(String)

    def __init__(self, message, datetime):
        self.message = message
        self.datetime = datetime

    def __repr__(self):  # pragma: no cover
        return "<{id}> Message: {message} - Date: {date}".format(id=self.id, message=self.message, date=self.datetime)


class GratitudeDatabaseController(object):

    def add_gratitude(self, message, datetime):
        logging.info("Adding a gratitude to database...")
        logging.debug("Message: {message} - Datetime: {datetime}".format(
            message=message, datetime=datetime
        ))
        gratitude = Gratitude(message, datetime)
        db.session.add(gratitude)
        db.session.commit()
        return gratitude

    def delete_gratitude(self, id):
        logging.info("Deleting a gratitude of id: {id} ...".format(id=id))
        gratitude = Gratitude.query.filter(Gratitude.id == id).first()
        db.session.delete(gratitude)
        db.session.commit()
        return gratitude

    def get_gratitudes(self, start_date=None, end_date=None):
        if start_date and end_date:
            logging.info("Getting all gratitudes from {start_date} to {end_date}...".format(
                start_date=start_date, end_date=end_date
            ))
            results = Gratitude.query.filter(Gratitude.datetime >= start_date, Gratitude.datetime <= end_date).all()
        else:
            logging.info("Getting all gratitudes...")
            results = Gratitude.query.all()
        # Sort the result based on dates
        sorted_result_by_date = sorted(results, key=lambda gratitude: gratitude.datetime, reverse=True)
        return sorted_result_by_date

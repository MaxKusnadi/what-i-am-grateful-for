import logging

from app import db
from sqlalchemy import Column, String, Integer, Text, Boolean


class Prayer(db.Model):
    __tablename__ = 'prayer'

    id = Column(Integer, primary_key=True)
    message = Column(Text)
    datetime = Column(String)
    isPrayed = Column(Boolean)

    def __init__(self, message, datetime):
        self.message = message
        self.datetime = datetime
        self.isPrayed = False

    def prayed(self):
        self.isPrayed = True

    def __repr__(self):  # pragma: no cover
        return "<{id}> Message: {message} - Date: {date} - isPrayed: {isPrayed}".format(
            id=self.id,
            message=self.message,
            date=self.datetime,
            isPrayed=self.isPrayed
        )


class PrayerDatabaseController(object):

    def add_prayer(self, message, datetime):
        logging.info("Adding a prayer to database...")
        logging.debug("Message: {message} - Datetime: {datetime}".format(
            message=message, datetime=datetime
        ))
        prayer = Prayer(message, datetime)
        db.session.add(prayer)
        db.session.commit()
        return prayer

    def delete_prayer(self, id):
        logging.info("Deleting a prayer of id: {id}...".format(id=id))
        prayer = Prayer.query.filter(Prayer.id == id).first()
        db.session.delete(prayer)
        db.session.commit()
        return prayer

    def pray_prayer(self, id):
        logging.info("Praying a prayer of id: {id}...".format(id=id))
        prayer = Prayer.query.filter(Prayer.id == id).first()
        prayer.prayed()
        db.session.commit()
        return prayer

    def get_prayed_prayer(self, start_date=None, end_date=None):
        if start_date and end_date:
            logging.info("Getting all prayed prayers from {start_date} to {end_date}...".format(
                start_date=start_date, end_date=end_date
            ))
            results = Prayer.query.filter(Prayer.datetime >= start_date)\
                                  .filter(Prayer.datetime <= end_date)\
                                  .filter(Prayer.isPrayed.is_(True)).all()
        else:
            logging.info("Getting all prayers...")
            results = Prayer.query.filter(Prayer.isPrayed.is_(True)).all()
        # Sort the result based on dates
        sorted_result_by_date = sorted(results, key=lambda prayer: prayer.datetime, reverse=True)
        return sorted_result_by_date

    def get_unprayed_prayer(self, start_date=None, end_date=None):
        if start_date and end_date:
            logging.info("Getting all unprayed prayers from {start_date} to {end_date}...".format(
                start_date=start_date, end_date=end_date
            ))
            results = Prayer.query.filter(Prayer.datetime >= start_date)\
                                  .filter(Prayer.datetime <= end_date)\
                                  .filter(Prayer.isPrayed.is_(False)).all()
        else:
            logging.info("Getting all prayers...")
            results = Prayer.query.filter(Prayer.isPrayed.is_(False)).all()
        # Sort the result based on dates
        sorted_result_by_date = sorted(results, key=lambda prayer: prayer.datetime, reverse=True)
        return sorted_result_by_date

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

import logging

from app import db
from sqlalchemy import Column, String, Integer, Text, Boolean


class Prayer(db.Model):
    __tablename__ = 'prayer'

    id = Column(Integer, primary_key=True)
    message = Column(Text)
    datetime = Column(String)
    isPrayed = Column(Boolean),

    def __init__(self, message, datetime):
        self.message = message
        self.datetime = datetime
        self.isPrayed = False

    def prayed(self):
        self.isPrayed = True

    def __repr__(self):  # pragma: no cover
        return "<{id}> Message: {message} - Date: {date}".format(id=self.id, message=self.message, date=self.datetime)

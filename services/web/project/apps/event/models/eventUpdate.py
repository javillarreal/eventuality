from datetime import datetime

from graphene_sqlalchemy import SQLAlchemyObjectType
from enum import IntEnum, auto

from project.app import db


class EventUpdate(db.Model):

    class Tag(IntEnum):
        GENERAL = auto()
        TICKETS = auto()
        DATES = auto()
        LINE_UP = auto()
        MERCH = auto()
        LOCATION = auto()

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    tag = db.Column(db.Integer, nullable=False, default=Tag.GENERAL.value)
    text = db.Column(db.Text)

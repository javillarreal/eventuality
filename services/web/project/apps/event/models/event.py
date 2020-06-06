from datetime import datetime
from enum import IntEnum

from project.app import db
from project.apps.promoter.models.promoter import Promoter


event_subcategories = db.Table('event_subcategories',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('event_category.id'), primary_key=True)
)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    longitude = db.Column(db.Float(precision=9))
    latitude = db.Column(db.Float(precision=9))
    datetime_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    datetime_to = db.Column(db.DateTime)
    capacity = db.Column(db.Integer, default=0)
    profit = db.Column(db.Boolean, default=False, nullable=False)
    subcateogries = db.relationship('EventCategory', secondary=event_subcategories)
    main_category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'))
    main_category = db.relationship('EventCategory')


    def __repr__(self):
        return f'Event: {self.name}'

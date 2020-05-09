from datetime import datetime

from project.app import db
from project.apps.promoter.models.promoter import Promoter


promoters = db.Table('promoters',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('promoter_id', db.Integer, db.ForeignKey('promoter.id'), primary_key=True),
    db.Column('role', db.Integer, default=1, nullable=False)
)

categories = db.Table('categories',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('event_category.id'), primary_key=True),
    db.Column('main', db.Boolean, default=False, nullable=False)
)


class Event(db.Model):
    PROMOTER_ROLES = {
        'copromoter': 0,
        'main': 1
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    longitude = db.Column(db.Float(precision=9))
    latitude = db.Column(db.Float(precision=9))
    datetime_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    datetime_to = db.Column(db.DateTime)
    promoters = db.relationship('Promoter', secondary=promoters)
    cateogries = db.relationship('EventCategory', secondary=categories)
    capacity = db.Column(db.Integer, default=0)


    def __repr__(self):
        promoter = Event.query.filter(
            Event.promoters.any(role=Event.PROMOTER_ROLES['main']),
            Event.id==self.id
        ).first()
        return f'Event: {self.name}, by {promoter.name}... '

from enum import IntEnum, auto
from project.app import db


class EventPromoter(db.Model):

    class Role(IntEnum):
        COPROMOTER = auto()
        MAIN = auto()

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    promoter_id = db.Column(db.Integer, db.ForeignKey('promoter.id'), primary_key=True)

    role = db.Column(db.Integer, default=1, nullable=False)

    event = db.relationship('Event', backref=db.backref('promoters'))
    promoter = db.relationship('Promoter', backref=db.backref('events', lazy='dynamic'))

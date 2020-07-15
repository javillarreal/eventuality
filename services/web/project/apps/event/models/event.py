from datetime import datetime
from enum import IntEnum, auto

from dateutil.relativedelta import relativedelta

from project.app import db
from project.apps.promoter.models.promoter import Promoter, PromoterUser
from project.apps.user.models.user import User

from .eventCategory import EventCategory

event_subcategories = db.Table('event_subcategories',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('event_category.id'), primary_key=True)
)


class Event(db.Model):
    minumum_duration = relativedelta(minutes=30)

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

    @classmethod
    def create_event(cls, user: User, main_promoters: list, copromoters: list = [], **kwargs):

        event = cls(**kwargs)
        db.session.add(event)
        db.session.commit()

        for promoter in main_promoters:
            event.assign_promoter(promoter=promoter, user=user, main=True)

        for promoter in copromoters:
            event.assign_promoter(promoter, user)

        return event
    
    def assign_promoter(self, promoter: Promoter, user: User, main: bool = False):

        event_promoter = EventPromoter(
            event=self,
            promoter=promoter,
            role=EventPromoter.Role.MAIN.value
        )
        
        user_role = promoter.get_user_role(user)

        if user_role >= PromoterUser.Role.CREATOR.value:
            event_promoter.status = EventPromoter.Status.APPROVED

        db.session.add(event_promoter)
        db.session.commit()


class EventPromoter(db.Model):

    class Role(IntEnum):
        COPROMOTER = auto()
        MAIN = auto()

    class Status(IntEnum):
        PENDING = auto()
        APPROVED = auto()
        REJECTED = auto()

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)
    promoter_id = db.Column(db.Integer, db.ForeignKey('promoter.id'), primary_key=True)

    role = db.Column(db.Integer, default=Role.MAIN.value, nullable=False)
    status = db.Column(db.Integer, default=Status.PENDING.value, nullable=False)

    event = db.relationship('Event', backref=db.backref('event_promoters'))
    promoter = db.relationship('Promoter', backref=db.backref('event_promoters', lazy='dynamic'))

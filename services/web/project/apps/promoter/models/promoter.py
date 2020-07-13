from datetime import datetime
from enum import IntEnum, auto
from sqlalchemy.ext.associationproxy import association_proxy

from project.app import db
from project.apps.event.models.eventCategory import EventCategory
from project.apps.user.models.user import User


class PromoterUser(db.Model):
    
    class Role(IntEnum):
        SUPPORT = auto()
        CREATOR = auto()
        ADMIN = auto()

    promoter_id = db.Column(db.Integer, db.ForeignKey('promoter.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    role = db.Column(db.Integer, default=1, nullable=False)

    promoter = db.relationship('Promoter', backref=db.backref('roles'))
    user = db.relationship('User', backref=db.backref('roles'))


class Promoter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    longitude = db.Column(db.Float(precision=9))
    latitude = db.Column(db.Float(precision=9))
    email = db.Column(db.String(40))
    category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'))
    category = db.relationship(EventCategory)
    users = db.relationship('User', secondary='promoter_user')
    # users = association_proxy("roles", "user")

    def __repr__(self):
        return f'<Promoter: {self.username}>'

    def get_user_role(self, user: User):
        promoter_user = PromoterUser.query.filter(PromoterUser.user==user)
        return promoter_user.role

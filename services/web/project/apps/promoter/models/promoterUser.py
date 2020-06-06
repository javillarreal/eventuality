from enum import IntEnum, auto

from graphene_sqlalchemy import SQLAlchemyObjectType

from project.app import db
from project.apps.promoter.models.promoter import Promoter
from project.apps.user.models.user import User


class PromoterUser(db.Model):
    
    class Role(IntEnum):
        SUPPORT = auto()
        CREATOR = auto()
        ADMIN = auto()

    promoter_id = db.Column(db.Integer, db.ForeignKey('promoter.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    role = db.Column(db.Integer, default=1, nullable=False)

    promoter = db.relationship(Promoter, backref=db.backref('users'))
    user = db.relationship(User, backref=db.backref('promoters'))


class PromoterUserType(SQLAlchemyObjectType):

    class Meta:
        model = PromoterUser

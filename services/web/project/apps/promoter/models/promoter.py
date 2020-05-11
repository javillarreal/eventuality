from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from project.app import db


class Promoter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    longitude = db.Column(db.Float(precision=9))
    latitude = db.Column(db.Float(precision=9))
    email = db.Column(db.String(40))
    main_category = db.Column(db.Integer, db.ForeignKey('event_category.id'))

    def __repr__(self):
        return f'<Promoter: {self.username}>'


class PromoterType(SQLAlchemyObjectType):

    class Meta:
        model = Promoter

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from project.app import db


class EventCategory(db.Model):
    __tablename__ = 'event_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String)
    default = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=True)
    children = db.relationship('EventCategory')

    def __repr__(self):
        return f'<Event category: {self.name}'

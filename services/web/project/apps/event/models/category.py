from flask_sqlalchemy import SQLAlchemy
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from project import db

class Category(db.Model):
    __tablename__ = 'event_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.String())
    default = db.Column(db.Boolean(), default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=True)
    children = db.relationship("Category")

    def __repr__(self):
        return f'<Event-category: {self.name}'


class CategoryType(SQLAlchemyObjectType):
    class Meta:
        model = Category

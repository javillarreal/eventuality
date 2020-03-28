from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
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
        return '<Event-category: {}'.format(self.name)

from datetime import datetime

from graphene_sqlalchemy import SQLAlchemyObjectType

from project.app import db


class EventUpdate(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    text = db.Column(db.Text)

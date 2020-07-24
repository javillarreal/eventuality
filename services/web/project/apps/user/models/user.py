from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from werkzeug.security import check_password_hash, generate_password_hash

from project.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(40), nullable=False, unique=True)

    country = db.Column(db.String(3))
    birthdate = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User: {self.username}>'

    @property
    def password(self):
        raise AttributeError('password not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self) -> str:
        return ' '.join(self.first_name, self.last_name)

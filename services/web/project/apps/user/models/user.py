from datetime import datetime

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from werkzeug.security import check_password_hash, generate_password_hash

from project.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, index=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(3))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime)
    birthdate = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

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

    def is_allowed(self, access_level) -> bool:
        return self.access >= access_level


class UserType(SQLAlchemyObjectType):
    full_name = graphene.String()

    class Meta:
        model = User
        exclude_fields = ('password_hash',)

    def resolve_full_name(parent, info):
        full_name = None

        if parent.first_name:
            full_name = parent.first_name

        if parent.last_name:
            last_name = parent.last_name
            if not full_name:
                full_name = last_name
            else:
                full_name = f'{full_name} {last_name}'
            
        return full_name

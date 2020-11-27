import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models.user import User


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

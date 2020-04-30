import graphene
from project.apps.user.models.user import User, UserType


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.query.all()

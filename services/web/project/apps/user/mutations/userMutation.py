import graphene
from project.app import db
from project.apps.user.models.user import User, UserType

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        birthdate = graphene.DateTime(required=False)
        country = graphene.String(required=False)
        # TODO: more arguments
    
    def mutate(self, info, **kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

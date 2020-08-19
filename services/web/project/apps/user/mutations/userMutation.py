import graphene

from project.app import db
from project.apps.user.models.user import User
from project.apps.user.exceptions import UserExceptions
from project.utils.graphql.input import get_model_fields, is_value_unique, resource_exists
from project.utils.graphql.mutation import BaseMutation
from flask_jwt_extended import create_access_token

from ..types import UserType


class LoginUser(BaseMutation):
    access_token = graphene.String()

    class Arguments:
        user_identifier = graphene.String(required=True)
        password = graphene.String(required=True)
    
    def mutate(self, info, user_identifier: str, password: str):
        exceptions = list()

        identifier = 'email' if '@' in user_identifier else 'username'

        result = resource_exists(User, user_identifier, identifier)
        if not isinstance(result, User):
            return LoginUser(exceptions=[result], success=False)
        user = result
        
        if not user.check_password(password):
            exceptions.append(UserExceptions.INVALID_CREDENTIAL.graphql)
        
        if len(exceptions) > 0:
            return LoginUser(exceptions=exceptions, success=False)
        
        access_token = create_access_token(identity=user.id)
        return LoginUser(access_token=access_token)


class CreateUser(BaseMutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        birthdate = graphene.DateTime(required=False)
        country = graphene.String(required=False)
        is_admin = graphene.Boolean(required=False)
        # TODO: more arguments

    def mutate(self, info, **kwargs):
        model_fields, other_fields = get_model_fields(User, **kwargs)

        exceptions = list()

        # check if username does not exists
        field = 'username'
        username = model_fields.pop(field)

        exception = is_value_unique(User, username, field)
        if exception is not None:
            exceptions.append(exception)
        
        # check if email does not exists
        field = 'email'
        email = model_fields.pop(field)

        exception = is_value_unique(User, email, field)
        if exception is not None:
            exceptions.append(exception)
        
        if len(exceptions) > 0:
            return CreateUser(exceptions=exceptions, success=False)

        user = User.create_user(**model_fields)

        return CreateUser(user=user)

# TODO: add modify user mutation


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()

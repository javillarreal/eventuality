import graphene

from project.app import db
from project.utils.auth.core import role_required
from project.apps.promoter.models.promoter import Promoter, PromoterUser
from project.apps.user.models.user import User
from project.utils.graphql.mutation import BaseMutation

from ..types import PromoterType, PromoterUserType

user_role_enum = graphene.Enum.from_enum(PromoterUser.Role)


class CreatePromoterUser(BaseMutation):
    promoter_user = graphene.Field(PromoterUserType)
    
    class Meta:
        description = 'This mutation will asign and existing user to a promoter with the specified role (default=creator)'
    
    class Arguments:
        promoter_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        role = graphene.Argument(user_role_enum, default_value=PromoterUser.Role.CREATOR)

    @role_required(required_role=PromoterUser.Role.ADMIN)
    def mutate(self, info, **kwargs):
        model_fields, _ = get_model_fields(Promoter, **kwargs)
        exceptions = list()

        # check if user exists
        field = 'promoter_id'
        promoter_id = model_fields.get(field)

        success, exception = is_valid_id(Promoter, promoter_id, field)
        if not success:
            exceptions.append(exception)

        # check if user exists
        field = 'user_id'
        user_id = model_fields.get(field)

        success, exception = is_valid_id(User, user_id, field)
        if not success:
            exceptions.append(exception)

        # return found exceptions
        if len(exceptions) > 0:
            return CreatePromoter(exceptions=exceptions, success=success)

        # assign user to promoter
        promoter_user = PromoterUser(model_fields)
        db.session.add(promoter_user)
        db.session.commit()

        return CreatePromoterUser(promoter_user=promoter_user)


class Mutation(graphene.ObjectType):
    create_promoter_user = CreatePromoterUser.Field()

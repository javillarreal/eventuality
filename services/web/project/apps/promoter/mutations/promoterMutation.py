import graphene

from project.apps.event.models.eventCategory import EventCategory
from project.apps.user.models.user import User
from project.apps.promoter.models.promoter import Promoter, PromoterType


class CreatePromoter(graphene.Mutation):
    promoter = graphene.Field(type=PromoterType)

    class Arguments:
        username = graphene.String(required=True)
        name = graphene.String(required=True)
        admin_user = graphene.Int(required=True)
        description = graphene.String(required=False)
        longitude = graphene.Float(required=False)
        latitude = graphene.Float(required=False)
        email = graphene.String(required=False)
        main_category = graphene.Int(required=False)

    
    def mutate(self, info, **kwargs):
        pass

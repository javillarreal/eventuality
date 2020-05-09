import graphene
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims
from project.utils.auth import admin_required

from ..models.eventCategory import EventCategory, EventCategoryType

class Query(graphene.ObjectType):
    # node = graphene.relay.Node.Field()
    # all_categories = SQLAlchemyConnectionField(CategoryType)
    categories = graphene.List(EventCategoryType)
    default_category = graphene.Field(EventCategoryType)
    
    @admin_required
    def resolve_categories(self, info):
        print(get_jwt_claims)
        print(get_jwt_identity())
        return EventCategory.query.all()

    def resolve_default_category(self, info):
        return EventCategory.query.filter_by(default=True).first()

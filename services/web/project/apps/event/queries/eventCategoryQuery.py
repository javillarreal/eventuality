import graphene
from flask_jwt_extended import get_jwt_claims, get_jwt_identity, jwt_required

from ..models.eventCategory import EventCategory
from ..types import EventCategoryType


class Query(graphene.ObjectType):
    # node = graphene.relay.Node.Field()
    # all_categories = SQLAlchemyConnectionField(EventCategoryType)
    categories = graphene.List(EventCategoryType)
    default_category = graphene.Field(EventCategoryType)
    
    def resolve_categories(self, info):
        print(get_jwt_claims())
        print(get_jwt_identity())
        return EventCategory.query.all()

    def resolve_default_category(self, info):
        return EventCategory.query.filter_by(default=True).first()

import graphene
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt_header

from ..models.category import Category, CategoryType

class Query(graphene.ObjectType):
    # node = graphene.relay.Node.Field()
    # all_categories = SQLAlchemyConnectionField(CategoryType)
    categories = graphene.List(CategoryType)
    default_category = graphene.Field(CategoryType)
    
    @jwt_required
    def resolve_categories(self, info):
        print(get_jwt_identity())
        return Category.query.all()

    def resolve_default_category(self, info):
        return Category.query.filter_by(default=True).first()

import graphene
# from graphene_sqlalchemy import SQLAlchemyConnectionField

from ..models.category import Category, CategoryType

class Query(graphene.ObjectType):
    # node = graphene.relay.Node.Field()
    # all_categories = SQLAlchemyConnectionField(CategoryType)
    categories = graphene.List(CategoryType)
    default_category = graphene.Field(CategoryType)

    def resolve_categories(self, info):
        return Category.query.all()

    def resolve_default_category(self, info):
        return Category.query.filter_by(default=True).first()

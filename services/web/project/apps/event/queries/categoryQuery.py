import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField

from ..models.category import CategoryType

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_categories = SQLAlchemyConnectionField(CategoryType)

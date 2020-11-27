from graphene_sqlalchemy import SQLAlchemyObjectType

from .models.promoter import Promoter, PromoterUser


class PromoterUserType(SQLAlchemyObjectType):

    class Meta:
        model = PromoterUser


class PromoterType(SQLAlchemyObjectType):

    class Meta:
        model = Promoter

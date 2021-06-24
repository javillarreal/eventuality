import graphene
from flask_jwt_extended import jwt_required
from project.utils.auth.core import admin_required

from ..models.promoter import Promoter
from ..types import PromoterType


class Query(graphene.ObjectType):
    promoters = graphene.List(PromoterType)
    
    @admin_required
    def resolve_promoters(self, info):
        return Promoter.query.all()

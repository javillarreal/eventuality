from inspect import getmembers

import graphene
from flask_jwt_extended import jwt_required

from project.app import db
from project.apps.event.models.eventCategory import EventCategory
from project.apps.promoter.models.promoter import Promoter, PromoterUser
from project.apps.user.models.user import User
from project.utils.auth.core import admin_required
from project.utils.graphql.input import (ExceptionType, get_model_fields,
                                         is_valid_id)
from project.utils.graphql.mutation import BaseMutation

from ..types import PromoterType


class CreatePromoter(BaseMutation):
    promoter = graphene.Field(PromoterType)

    class Arguments:
        username = graphene.String(required=True)
        name = graphene.String(required=True)
        admin_user_id = graphene.Int(required=True)
        description = graphene.String(required=False)
        longitude = graphene.Float(required=False)
        latitude = graphene.Float(required=False)
        email = graphene.String(required=False)
        category_id = graphene.Int(required=False)
        subcategories_ids = graphene.List(graphene.Int, required=False)

    @admin_required    
    def mutate(self, info, **kwargs):
        model_fields, other_fields = get_model_fields(Promoter, **kwargs)
        exceptions = list()

        # check if user exists
        field = 'admin_user_id'
        admin_user_id = other_fields.get(field)

        exception = is_valid_id(User, admin_user_id, field)
        if exception is not None:
            exceptions.append(exception)
        else:
            admin_user = User.query.get(admin_user_id)
        
        # check if username is available
        field = 'username'
        promoter_username = model_fields.get(field)
        if Promoter.query.filter(Promoter.username==promoter_username).first():
            exception = ExceptionType(
                field=field,
                message=f"'{promoter_username}' {field} is taken"
            )
            exceptions.append(exception)

        # check if event_category exists
        field = 'category_id'
        category_id = model_fields.get(field, None)

        if category_id:
            exception = is_valid_id(EventCategory, category_id, field)
            if exception is not None: exceptions.append(exception)

        if len(exceptions) > 0:
            return CreatePromoter(exceptions=exceptions, ok=False)
        
        # create promoter
        promoter = Promoter(**model_fields)
        db.session.add(promoter)
        db.session.commit()
        
        # assign user to promoter
        promoter_user = PromoterUser(
            promoter=promoter,
            user=admin_user,
            role=PromoterUser.Role.ADMIN
        )
        db.session.add(promoter)
        db.session.commit()
        
        return CreatePromoter(promoter=promoter)


class Mutation(graphene.ObjectType):
    create_promoter = CreatePromoter.Field()

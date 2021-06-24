import graphene
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

from project.app import db
from project.apps.promoter.models.promoter import Promoter, PromoterUser
from project.apps.user.models.user import User
from project.utils.auth.core import role_required
from project.utils.graphql.exception import ExceptionType
from project.utils.graphql.input import (get_model_fields, is_valid_id,
                                         validate_dates)
from project.utils.graphql.mutation import BaseMutation

from ..models.event import Event
from ..models.eventCategory import EventCategory
from ..types import EventCategoryType, EventType


class CreateEvent(BaseMutation):
    # TODO: add inputs for co-promoters
    # TODO: add checks for limit of posted events
    event = graphene.Field(EventType)

    class Arguments:
        name = graphene.String(required=True)
        longitude = graphene.Float(required=False)
        latitude = graphene.Float(required=False)
        # TODO: make it required
        datetime_from = graphene.DateTime(required=False, default_value=datetime.now())
        datetime_to = graphene.DateTime(required=False)
        capacity = graphene.Int(required=False)
        profit = graphene.Boolean(required=False)
        main_category_id = graphene.Int(required=True)
        subcategories_ids = graphene.List(graphene.Int, required=False)
        main_promoters_ids = graphene.List(graphene.Int, required=True)
        copromoters_ids = graphene.List(graphene.Int, required=False)

    # TODO: add location support
    @role_required(required_role=PromoterUser.Role.CREATOR)
    def mutate(self, info, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        model_fields, other_fields = get_model_fields(Event, **kwargs)
        exceptions = list()
        print(model_fields)


        exception = validate_dates(
            model_fields.get('datetime_from'), 
            model_fields.get('datetime_to')
        )
        if exception is not None:
            print(exceptions)
            exceptions.append(exception)
        
        capacity = model_fields.get('capacity')
        if capacity is not None:
            if capacity < 0:
                exception = ExceptionType(
                    field='capacity',
                    message=f'Capacity must be more than 0. Received {capacity}'
                )
                exceptions.append(exception)

        # check if main category exists
        field = 'main_category_id'
        main_category_id = model_fields.get(field)

        exception = is_valid_id(EventCategory, main_category_id, field)
        if exception is not None:
            exceptions.append(exception)
        else:
            main_category = EventCategory.query.get(main_category_id)

        # check if main promoters exists
        field = 'main_promoters_ids'
        main_promoters_ids = other_fields.get(field)

        main_promoters = list()
        for promoter_id in main_promoters_ids:
            exception = is_valid_id(Promoter, promoter_id, field)

            if exception is not None:
                exceptions.append(exception)
            else:
                main_promoters.append(Promoter.query.get(promoter_id))

        print([str(e.message) for e in exceptions])
        if len(exceptions) > 0:
            return CreateEvent(exceptions=exceptions, success=False)
        
        event = Event.create_event(user=user, main_promoters=main_promoters, **model_fields)

        return CreateEvent(event=event)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()

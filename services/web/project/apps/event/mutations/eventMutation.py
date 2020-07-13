import graphene

from project.app import db
from project.apps.promoter.models.promoter import PromoterUser
from project.utils.auth.core import requires_access_level, role_required
from project.utils.graphql.input import (get_model_fields, is_valid_id,
                                         validate_dates)
from project.utils.graphql.mutation import BaseMutation

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
        datetime_from = graphene.DateTime(required=True)
        datetime_to = graphene.DateTime(required=False)
        capacity = graphene.Int(required=False)
        profit = graphene.Boolean(required=False)
        main_category_id = graphene.Int(required=True)
        subcategories_ids = graphene.List(graphene.Int, required=False)
        
    # TODO: add decorator for creator and admin roles requirement
    @requires_access_level(required_role=PromoterUser.Role.CREATOR)
    def mutate(self, info, **kwargs):
        # TODO: add location support
        model_fields, other_fields = get_model_fields(Event, **kwargs)
        exceptions = list()

        ok, exception = validate_dates(
            model_fields.get('datetime_from'), 
            model_fields.get('datetime_to')
        )
        if ok is False:
            exceptions.append(exception)
        
        capacity = model_fields.get('capacity')
        if capacity is not None:
            if capacity < 0:
                ok = False
                exception = ExceptionType(
                    field='capacity',
                    message=f'Capacity must be grater than 0. Received {capacity}'
                )

         # check if user exists
        field = 'main_category_id'
        main_category_id = model_fields.get(field)

        ok, exception = is_valid_id(EventCategory, main_category_id, field)
        if not ok:
            exceptions.append(exception)
        else:
            main_category = EventCategory.query.get(main_category_id)

        if len(exceptions) > 0:
            return CreateEvent(exceptions=exceptions, ok=ok)

        # create event
        event = Event(**model_fields)
        # db.session.add(event)
        # db.session.commit()

        return CreateEvent(event=event)


class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()

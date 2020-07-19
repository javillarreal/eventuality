import graphene

from project.app import db
from project.apps.promoter.models.promoter import PromoterUser
from project.utils.auth.core import role_required
from project.utils.graphql.input import (get_model_fields, is_valid_id)
from project.utils.graphql.mutation import BaseMutation

from ..models.event import Event
from ..models.eventUpdate import EventUpdate
from ..types import EventUpdateType


class CreateEventUpdate(BaseMutation):
    event_update = graphene.Field(EventUpdateType)

    class Arguments:
        event_id = graphene.Int(required=True)
        text = graphene.String(required=True)
    
    @role_required(required_role=PromoterUser.Role.CREATOR)
    def mutate(self, info, **kwargs):
        model_fields, other_fields = get_model_fields(EventUpdate, **kwargs)

        exceptions = list()
        
        # check if event exists
        field = 'event_id'
        event_id = model_fields.pop(field)

        exception = is_valid_id(Event, event_id, field)
        if exception is not None:
            exceptions.append(exception)
        else:
            event = Event.query.get(event_id)
        
        if len(exceptions) > 0:
            print(exceptions)
            return CreateEventUpdate(ok=Falase, exceptions=exceptions)
        
        event_update = event.create_update(**model_fields)

        return CreateEventUpdate(event_update=event_update)


class Mutation(graphene.ObjectType):
    create_event_update = CreateEventUpdate.Field()

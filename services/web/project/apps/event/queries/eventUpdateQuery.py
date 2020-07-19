import graphene

from project.apps.event.types import EventUpdateType
from project.apps.event.models.eventUpdate import EventUpdate


class Query(graphene.ObjectType):
    event_uptades = graphene.List(EventUpdateType, event_id=graphene.Int(required=True))

    def resolve_event_uptades(self, info, event_id):
        return EventUpdate.query.filter(EventUpdate.event_id==event_id).all()

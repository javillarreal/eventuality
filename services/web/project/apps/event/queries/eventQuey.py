import graphene

from ..models.event import Event
from ..types import EventType


class Query(graphene.ObjectType):
    events = graphene.List(EventType)
    
    def resolve_events(self, info):
        return Event.query.all()

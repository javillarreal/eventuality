import graphene

from ..models.event import Event
from ..types import EventType


class Query(graphene.ObjectType):
    events = graphene.List(
        EventType,
        main_category_id=graphene.Int(required=False)
    )
    event = graphene.Field(
        EventType,
        id=graphene.Int(required=True)
    )
    
    def resolve_events(self, info, **kwargs):
        events_query = Event.query
        for field, value in kwargs.items():
            events_query = events_query.filter(getattr(Event, field)==value)
        
        return events_query.all()
    
    def resolve_event(self, info, id: int):
        return Event.query.get(id)

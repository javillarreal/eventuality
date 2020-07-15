import graphene

from ..models.event import Event
from ..types import EventType


class Query(graphene.ObjectType):
    events = graphene.List(EventType)
    
    def resolve_categories(self, info):
        print('events')
        return Event.query.all()

    def resolve_default_category(self, info):
        return EventCategory.query.filter_by(default=True).first()

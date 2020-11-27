import graphene

from project.apps.event.types import EventUpdateType
from project.apps.event.models.eventUpdate import EventUpdate


class Query(graphene.ObjectType):
    event_uptades = graphene.List(EventUpdateType, 
        event_id=graphene.Int(required=True),
        tag=graphene.Argument(EventUpdateType.tag_enum, required=False)
    )

    def resolve_event_uptades(self, info, **kwargs):
        updates_query = EventUpdate.query
        for field, value in kwargs.items():
            updates_query = updates_query.filter(getattr(EventUpdate, field)==value)
        
        return updates_query.all()

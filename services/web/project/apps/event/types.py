from graphene_sqlalchemy import SQLAlchemyObjectType

from .models.event import Event
from .models.eventCategory import EventCategory


class EventType(SQLAlchemyObjectType):
    
    class Meta:
        model = Event


class EventCategoryType(SQLAlchemyObjectType):
    
    class Meta:
        model = EventCategory

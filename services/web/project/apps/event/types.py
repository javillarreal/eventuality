from graphene_sqlalchemy import SQLAlchemyObjectType

from .models.event import Event, EventPromoter
from .models.eventCategory import EventCategory


class EventType(SQLAlchemyObjectType):
    
    class Meta:
        model = Event


class EventPromoterType(SQLAlchemyObjectType):
    
    class Meta:
        model = EventPromoter


class EventCategoryType(SQLAlchemyObjectType):
    
    class Meta:
        model = EventCategory

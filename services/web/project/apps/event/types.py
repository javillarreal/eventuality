import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from .models.event import Event, EventPromoter
from .models.eventCategory import EventCategory
from .models.eventUpdate import EventUpdate


class EventType(SQLAlchemyObjectType):
    
    class Meta:
        model = Event


class EventPromoterType(SQLAlchemyObjectType):
    
    class Meta:
        model = EventPromoter


class EventCategoryType(SQLAlchemyObjectType):
    
    class Meta:
        model = EventCategory


class EventUpdateType(SQLAlchemyObjectType):
    tag_enum = graphene.Enum.from_enum(EventUpdate.Tag)

    class Meta:
        model = EventUpdate

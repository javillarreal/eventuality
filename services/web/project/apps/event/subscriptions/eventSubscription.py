import graphene

from ..types import EventType

class Subscription(graphene.ObjectType):
    event = graphene.Field(EventType)

    def resolve_event():
        pass


# from sqlalchemy import event
# 
# # standard decorator style
# @event.listens_for(SomeClass, 'after_insert')
# def receive_after_insert(mapper, connection, target):
#     "listen for the 'after_insert' event"
# 
#     # ... (event handling logic) ...
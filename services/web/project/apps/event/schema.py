from .mutations import eventMutation, eventUpdateMutation
from .queries import eventCategoryQuery, eventQuey, eventUpdateQuery
from .subscriptions import eventUpdateSubscription


class EventQuery(eventQuey.Query, eventCategoryQuery.Query, eventUpdateQuery.Query):
    pass


class EventMutation(eventMutation.Mutation, eventUpdateMutation.Mutation):
    pass


class EventSubscription(eventUpdateSubscription.Subscription):
    pass

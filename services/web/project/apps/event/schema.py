from .mutations import eventMutation
from .queries import eventCategoryQuery


class EventQuery(eventCategoryQuery.Query):
    pass


class EventMutation(eventMutation.Mutation):
    pass

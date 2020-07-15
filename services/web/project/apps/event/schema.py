from .mutations import eventMutation
from .queries import eventCategoryQuery, eventQuey


class EventQuery(eventQuey.Query, eventCategoryQuery.Query):
    pass


class EventMutation(eventMutation.Mutation):
    pass

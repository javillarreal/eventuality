from .mutations import userMutation
from .queries import userQuery


class UserQuery(userQuery.Query):
    pass


class UserMutation(userMutation.Mutation):
    pass

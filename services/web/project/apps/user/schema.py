from .queries import userQuery
from .mutations import userMutation

class UserQuery(userQuery.Query):
    pass


class UserMutation(userMutation.Mutation):
    pass

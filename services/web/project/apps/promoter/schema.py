from .mutations import promoterMutation, promoterUserMutation
from .queries import promoterQuery


class PromoterQuery(promoterQuery.Query):
    pass


class PromoterMutation(promoterMutation.Mutation, promoterUserMutation.Mutation):
    pass

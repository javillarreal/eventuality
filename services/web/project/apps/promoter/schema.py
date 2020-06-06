from .queries import promoterQuery

from .mutations import promoterMutation
from .mutations import promoterUserMutation


class PromoterQuery(promoterQuery.Query):
    pass


class PromoterMutation(promoterMutation.Mutation, promoterUserMutation.Mutation):
    pass

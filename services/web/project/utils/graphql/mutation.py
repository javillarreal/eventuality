import graphene

from project.utils.graphql.exception import ExceptionType


class BaseMutation(graphene.Mutation):
    success = graphene.Boolean(required=True, default_value=True)
    exceptions = graphene.List(ExceptionType)

    class Meta:
        abstract = True

    def mutate(self, info, **kwargs):
        """
        this method should be overrided for the moment
        """
        pass

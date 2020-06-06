import graphene


class ExceptionType(graphene.ObjectType):
    field = graphene.String(required=False, description='field causing the error (optional)')
    message = graphene.String(required=True, description='error message')

    class Meta:
        description = 'return this object if any kind of error appears during mutation'

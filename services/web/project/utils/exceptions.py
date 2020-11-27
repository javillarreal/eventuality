from enum import Enum
from .graphql.exception import ExceptionType

class BaseException(Enum):

    def __new__(cls, code, message, field=None):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.code = code
        obj.field = field
        obj.message = message
        return obj
    
    @property
    def graphql(self):
        return ExceptionType(
            code=self.code,
            field=self.field,
            message=self.message,
        )

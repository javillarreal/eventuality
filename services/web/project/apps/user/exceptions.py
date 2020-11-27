from project.utils.exceptions import BaseException

class UserExceptions(BaseException):
    INVALID_CREDENTIAL = '01-1', 'Incorrect password', 'password'

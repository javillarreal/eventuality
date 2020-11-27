class PermissionDenied(Exception):
    default_message = 'Unknown error ocurred'

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class AdminLevelRequired(PermissionDenied):
    default_message = 'Admin level required to perform this action'


class UserRoleNotSufficed(PermissionDenied):
    default_message = 'The user does not have the required role to perform this action'

class RedashPyException(Exception):
    """base exception"""


class ParameterException(RedashPyException):
    """param error"""


class ResourceNotFoundException(RedashPyException):
    """ not found """


class ErrorResponseException(RedashPyException):
    def __init__(self, *args, status_code):
        super().__init__(*args)
        self.status_code = status_code

    def __str__(self):
        msg = super().__str__()
        return f'[status:{self.status_code}]: f{msg}'

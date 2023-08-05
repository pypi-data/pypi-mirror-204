class DjangoPermTransCustomBaseException(Exception):
    message = 'An error occurred'

    def __init__(self, message=None, *args):
        message = message or self.message
        super().__init__(message, *args)


class DjangoPermTransCustomFuncException(DjangoPermTransCustomBaseException):
    message = '"DJANGO_PERM_TRANS.custom_function" property needs to be a function'

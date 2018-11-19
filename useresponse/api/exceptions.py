class APIException(Exception):
    """Base class for all API Exceptions"""
    pass


class ClientException(APIException):
    def __init__(self, response):
        self.response = response
        super(APIException, self).__init__(self, response)


class InvalidRequestException(ClientException):
    """400"""
    pass


class UnauthenticatedException(ClientException):
    """401"""
    pass


class UnauthorizedException(ClientException):
    """403"""
    pass


class OperationConflictException(ClientException):
    """409
    Whenever a resource conflict would be caused by fulfilling the request.
    Duplicate entries, deleting root objects when cascade-delete not supported
    are a couple of examples.
    """
    pass


class ServerError(APIException):
    def __init__(self, response):
        self.response = response
        super(APIException, self).__init__(self, response)


class InternalServerError(ServerError):
    """500"""
    pass


class ServiceUnavailableError(ServerError):
    """503"""
    pass

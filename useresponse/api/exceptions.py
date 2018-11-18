class APIException(Exception):
    """Base class for all API Exceptions"""
    pass


class InvalidRequestException(APIException):
    """400"""
    pass


class UnauthenticatedException(APIException):
    """401"""
    pass


class UnauthorizedException(APIException):
    """403"""
    pass


class OperationConflictException(APIException):
    """409
    Whenever a resource conflict would be caused by fulfilling the request.
    Duplicate entries, deleting root objects when cascade-delete not supported
    are a couple of examples.
    """
    pass


class InternalServerError(APIException):
    """500"""
    pass


class ServiceUnavailableError(APIException):
    """503"""
    pass

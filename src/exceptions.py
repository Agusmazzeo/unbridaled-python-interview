class CustomException(Exception):
    pass


class ConnectionFailure(CustomException):
    """Raised when the database connection fails"""

    pass


class QueryFailure(CustomException):
    """Raised when a query execution fails"""

    pass

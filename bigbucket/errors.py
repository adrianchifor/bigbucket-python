class RequestError(Exception):
    """Generic request error or 500 response from server"""
    pass


class ConnectionError(RequestError):
    """Connection refused to server"""
    pass


class Timeout(RequestError):
    """Request timeout"""
    pass


class TooManyRedirects(RequestError):
    """Request redirected too many times"""
    pass


class NotFound(RequestError):
    """Request response is 404"""
    pass

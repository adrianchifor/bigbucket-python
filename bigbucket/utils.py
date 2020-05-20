import requests

from bigbucket.errors import ConnectionError, Timeout, TooManyRedirects, NotFound, RequestError


def parse_response(response):
    try:
        json_response = response.json()
    except ValueError:
        raise RequestError(
            f"{response.status_code}: Invalid response from server")

    if response.status_code == 404:
        raise NotFound(f"{response.status_code}: {json_response['error']}")
    if response.status_code != 200:
        raise RequestError(f"{response.status_code}: {json_response['error']}")

    return json_response


def handle_exception(exception):
    if isinstance(exception, requests.exceptions.ConnectionError):
        raise ConnectionError(exception)
    elif isinstance(exception, requests.exceptions.Timeout):
        raise Timeout(exception)
    elif isinstance(exception, requests.exceptions.TooManyRedirects):
        raise TooManyRedirects(exception)
    else:
        raise RequestError(exception)

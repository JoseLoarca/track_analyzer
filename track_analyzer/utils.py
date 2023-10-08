import logging
from typing import Optional

import requests
from requests import RequestException
from requests.auth import AuthBase

from .exceptions import (SpotifyForbiddenOperationError,
                         SpotifyUnauthorizedError,
                         SpotifyLimitExceededError,
                         SpotifyUnknownStatusError)

# A list of the currently supported HTTP methods
SUPPORTED_METHODS = ['GET']


class SpotifyAuthHeaders(AuthBase):
    """Attaches a Bearer token to every Spotify request
    """

    def __init__(self, access_token: str):
        """Create a SpotifyAuthHeaders instance

        Args:
            access_token (str): the Spotify access token for authentication
        """
        self._access_token = access_token

    def __call__(self, req):
        """Modify the request headers and return it
        """
        req.headers['Authorization'] = f"Bearer {self._access_token}"
        return req


def make_http_request(base_url: str, path: str, access_token: str, query_params: Optional[dict] = None,
                      method: str = 'GET') -> dict:
    """Make a new HTTP request to the Spotify API using the path, query_params and method provided.

    Since the access_token is expected, this function is only intended to be used with authorized Spotify API calls. Any
    call to the Spotify API for authorization should be handled separately.

    TODO:
        Add support for POST requests.
        Implement a retry mechanism for errors returned by the Spotify API

    Args:
        base_url (str): the base URL for the request
        path (str): the path for the request
        access_token (str): the access token for authorization
        query_params (Optional[dict]): optional query params to be sent
        method (str): the method for the request

    Returns:
        dict: the JSON representation of the API response

    Raises:
        RequestException: if an unhandled error is raised by requests
        SpotifyUnauthorizedError: if an authorization error is returned by the Spotify API
        SpotifyForbiddenOperationError: if a forbidden error is returned by the Spotify API
        SpotifyLimitExceededError: if a rate limit exceeded error is returned by the Spotify API
        SpotifyUnknownStatusError: if an unhandled HTTP status code is returned by the Spotify API
    """
    # Make sure only the supported methods are used
    assert method in SUPPORTED_METHODS, f"{method} method not supported yet."

    # Handle GET requests
    try:
        if method == 'GET':
            response = requests.get(f"{base_url}/{path}", params=query_params, auth=SpotifyAuthHeaders(access_token))

    except RequestException as e:
        logging.critical(f"An unexpected error has occurred when trying to make a request to the Spotify API. {e=}")
        raise

    if response.status_code == requests.codes.ok:  # 200 OK
        return response.json()

    if response.status_code == requests.codes.unauthorized:  # 401 Unauthorized
        logging.error(f"Spotify returned {response.status_code} status.")
        raise SpotifyUnauthorizedError(path)

    elif response.status_code == requests.codes.forbidden:  # 403 Forbidden
        logging.error(f"Spotify returned {response.status_code} status.")
        raise SpotifyForbiddenOperationError(path)

    elif response.status_code == requests.codes.too_many_requests:  # 429 Too Many Requests
        logging.error(f"Spotify returned {response.status_code} status.")
        raise SpotifyLimitExceededError

    else:
        logging.error(f"Spotify returned {response.status_code} status.")
        raise SpotifyUnknownStatusError(method, path, response.status_code)  # Any other HTTP status code

from typing import Optional


class SpotifyException(Exception):
    """Base Spotify exception
    """
    pass


class SpotifyAuthenticationError(SpotifyException):
    """Exception raised for Spotify authentication errors
    """

    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Spotify authentication returned a {status_code} status code.")


class SpotifyForbiddenOperationError(SpotifyException):
    """Exception raised for Spotify's forbidden error
    """

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Spotify has forbidden the access to: {path}.")


class SpotifyUnauthorizedError(SpotifyException):
    """Exception raised for Spotify's unauthorized error.

    The difference between this and the forbidden error, is that when the forbidden error occurs the request's
    authorization is successful but the user lacks access to the resource. When an unauthorized error occurs, the
    request's authorization was never successful.
    """

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Could not authorize the request to Spotify's {path}.")


class SpotifyLimitExceededError(SpotifyException):
    """Exception raised for Spotify's rate limit exceeded error
    """

    def __init__(self):
        super().__init__(f"The app has exceeded its rate limits. Try again later.")


class SpotifyUnknownStatusError(SpotifyException):
    """Exception raised for unknown status codes returned by Spotify
    """

    def __init__(self, method: str, path: str, status_code: int):
        self.method = method
        self.path = path
        self.status_code = status_code
        super().__init__(f"The {method} request to Spotify's {path} has returned an unknown status code: {status_code}")


class SpotifyInvalidContentError(SpotifyException):
    """Exception raised if invalid content is found in the Spotify API responses.

    Examples:
        When searching for a track, the Spotify API should return a field named "tracks", if this field is not returned,
        we raise an error.
    """

    def __init__(self, method: str, path: str, error: Optional[str] = None):
        self.method = method
        self.path = path
        self.error = error

        exception_message = f"The {method} request to Spotify's {path} has returned a response with invalid content." \
            if not error \
            else f"The {method} request to Spotify's {path} has returned a response with invalid content. {error}"
        super().__init__(exception_message)

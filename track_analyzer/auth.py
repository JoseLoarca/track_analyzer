import time
import logging
import requests
from typing import NamedTuple, Optional

from .exceptions import SpotifyAuthenticationError


class SpotifyAccessToken(NamedTuple):
    """Represents a Spotify access token.

    The SpotifyAccessToken consists of:
    * access_token (str): the access token
    * expires_in (int): the duration of the token in seconds, eg: 3600 for 1hr
    * timestamp (time): the timestamp when the access token was generated
    """
    access_token: str
    expires_in: int
    timestamp: time = time.time()


class SpotifyAuth:
    """This class handles the authentication for the Spotify API.
    """

    def __init__(self, client_id: str, client_secret: str):
        """Create a SpotifyAuth instance

        Args:
            client_id (str): the Spotify's Client ID obtained from the Developer dashboard
            client_secret (str): the Spotify's Client Secret obtained from the Developer dashboard
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_url = 'https://accounts.spotify.com/api/token'

        # Store token
        self._credentials: Optional[SpotifyAccessToken] = None

    @property
    def access_token(self) -> str:
        """Property method for access_token. This method will take care of generating a new access_token if:
        * A token has never been generated before, or
        * A token has already been generated, but it has expired

        Returns: a valid access_token for using the Spotify API
        """
        if not self._credentials:
            self._generate_access_token()
            return self._credentials.access_token
        else:
            # Check if token is not expired yet
            current_time = time.time()
            token_timestamp = self._credentials.timestamp
            token_expiration_in_seconds = self._credentials.expires_in

            if (current_time - token_timestamp) > token_expiration_in_seconds:
                # Token has  expired
                self._generate_access_token()

            return self._credentials.access_token

    def _generate_access_token(self) -> None:
        """Generate a new access token
        """
        body = {"grant_type": "client_credentials", "client_id": self._client_id, "client_secret": self._client_secret}
        req = requests.post(self._auth_url, data=body)

        if req.status_code == requests.codes.ok:
            resp = req.json()
            self._credentials = SpotifyAccessToken(access_token=resp.get("access_token"),
                                                   # Subtract 5 seconds just in case
                                                   expires_in=(resp.get("expires_in") - 5))
            logging.info('Access token generated successfully.')
        else:
            logging.error(f"Could not generate access token. Status code: {req.status_code}")
            raise SpotifyAuthenticationError(req.status_code)

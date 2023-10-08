from .auth import SpotifyAuth


class SpotifyClient:
    """This class will handle authenticated requests to the Spotify API
    """

    def __init__(self, client_id: str, client_secret: str):
        """Create a SpotifyClient instance

        Args:
            client_id (str): the Spotify's Client ID obtained from the Developer dashboard
            client_secret (str): the Spotify's Client Secret obtained from the Developer dashboard
        """
        self.auth = SpotifyAuth(client_id, client_secret)
        self.base_url = 'https://api.spotify.com/v1/'


class SpotifyAuthenticationError(Exception):
    """Exception raised for Spotify authentication errors
    """
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Spotify authentication returned a {status_code} status code.")

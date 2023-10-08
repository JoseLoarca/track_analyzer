from typing import Optional


class SpotifyArtist:
    """This class represents a Spotify artist
    """

    def __init__(self,
                 name: str,
                 artist_id: str,
                 *,

                 followers: Optional[int] = None,
                 genres: Optional[list[str]] = None,
                 image_url: Optional[str] = None,
                 popularity: Optional[int] = None):
        """Create a new SpotifyArtist instance

        Args:
            name (str): the name of the artist
            artist_id (str): the Spotify ID of the artist
            -
            followers (Optional[int]): the total amount of followers of the artist
            genres (Optional[list[str]]): the list of genres associated to the artist
            image_url (Optional[str]): the image URL of the artist
            popularity (Optional[int]): the popularity of the artist, this should be a value from 0 to 100,
                with 100 being the most popular
        """
        # If provided, make sure popularity is between 0 and 100
        if popularity is not None and not (0 <= popularity <= 100):
            raise ValueError("The popularity of the artist should be between 0 and 100.")

        self.name = name
        self.artist_id = artist_id
        # Keyword args:
        self.followers = followers
        self.genres = genres
        self.image_url = image_url
        self.popularity = popularity

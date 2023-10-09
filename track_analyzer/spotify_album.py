from typing import Optional, NamedTuple

# A list of the allowed album types
ALLOWED_ALBUM_TYPES = ["single", "album", "compilation"]


class SpotifyAlbumReleaseDate(NamedTuple):
    """Represents the release date of a Spotify album

    The SpotifyAlbumReleaseDate consists of:
    * released_on (str): the date the album was first released, eg: "1997", "2006-01" or "2023-01-01"
    * precision (str): the precision of the released_on value, this can be: day, month or year
    """
    released_on: str
    precision: str  # day, month or year


class SpotifyAlbum:
    """This class represents a Spotify album
    """

    def __init__(self,
                 name: str,
                 album_id: str,
                 *,

                 album_type: Optional[str] = None,
                 genres: Optional[list[str]] = None,
                 image_url: Optional[str] = None,
                 popularity: Optional[int] = None,
                 total_tracks: Optional[int] = None,
                 label: Optional[str] = None,
                 release_date: Optional[SpotifyAlbumReleaseDate] = None
                 ):
        """Create a new SpotifyAlbum instance

        Args:
            name (str): the name of the album
            album_id (str): the Spotify ID of the album
            -
            album_type (Optional[str]): the album type, this value can be: album, single or compilation
            genres (Optional[list[str]]): the list of genres associated to the album
            image_url (Optional[str]): the image URL of the album
            popularity (Optional[int]): the popularity of the album, this should be a value from 0 to 100,
                with 100 being the most popular
            total_tracks (Optional[int]): the number of tracks the album has
            label (Optional[str]): the label associated to the album
            release_date (Optional[SpotifyAlbumReleaseDate]): the album's release date
        """
        # If provided, make sure album_type is a valid album type
        if album_type is not None and album_type not in ALLOWED_ALBUM_TYPES:
            raise ValueError(f"{album_type} is not a valid album type.")

        # If provided, make sure popularity is between 0 and 100
        if popularity is not None and not (0 <= popularity <= 100):
            raise ValueError("The popularity of the artist should be between 0 and 100.")

        self.name = name
        self.album_id = album_id
        # Keyword args:
        self.album_type = album_type
        self.genres = genres
        self.image_url = image_url
        self.popularity = popularity
        self.total_tracks = total_tracks
        self.label = label
        self.release_date = release_date

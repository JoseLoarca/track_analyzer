import logging
import os
from typing import Optional

from track_analyzer.auth import SpotifyAuth
from track_analyzer.exceptions import SpotifyInvalidContentError
from track_analyzer.spotify_album import SpotifyAlbum, SpotifyAlbumReleaseDate
from track_analyzer.spotify_artist import SpotifyArtist
from track_analyzer.spotify_track import SpotifyTrack
from track_analyzer.utils import make_http_request

DEFAULT_MARKET: str = os.environ.get('DEFAULT_MARKET', 'GT')  # Default the market to Guatemala

# Spotify's object types:
TRACK: str = "track"

# Spotify's paths:
SEARCH: str = "search"


class SpotifyClient:
    """This class will handle authenticated requests to the Spotify API
    """

    def __init__(self, client_id: str, client_secret: str):
        """Create a SpotifyClient instance

        Args:
            client_id (str): the Spotify's Client ID obtained from the Developer dashboard
            client_secret (str): the Spotify's Client Secret obtained from the Developer dashboard
        """
        self._auth = SpotifyAuth(client_id, client_secret)
        self.base_url = 'https://api.spotify.com/v1'

    def search_track(self,
                     query: str,
                     market: Optional[str] = None,
                     include_artists: bool = True,
                     include_album: bool = True) -> Optional[SpotifyTrack]:
        """Search for a track using the Spotify API. Currently, this search is limited to a single return value,
        meaning that if a matching track is found, then it is returned, else nothing is returned.

        Args:
            query (str): the name of the track to use in the search
            market (Optional[str]): a country code. If a value is specified, only content that is available in the
                market will be returned.
            include_artists (bool): if returned, populate the artists information in the returned SpotifyTrack,
                defaults to True
            include_album (bool): if returned, populate the album information in the returned SpotifyTrack,
                defaults to True

        Returns: if a matching track was found, a SpotifyTrack instance is returned, else None
        """
        # Build the query params for the request
        query_params = {
            "type": TRACK,
            "market": market if market else DEFAULT_MARKET,
            "limit": 1,
            "q": query
        }
        # Make the HTTP request
        result = make_http_request(self.base_url, SEARCH, self._auth.access_token, query_params)

        if "tracks" not in result:  # Return an error if "tracks" is not in the response
            raise SpotifyInvalidContentError("GET", SEARCH, "'tracks' is missing in the response.")

        tracks_section = result.get("tracks")
        if not tracks_section.get("items"):  # Empty items means no matching track was found
            logging.error(f"Could not find any matching track with the given query: {query}")
            return None

        # Extract the track info from the response
        track_info_from_response = tracks_section.get("items")[0]
        logging.info('Matching track found, extracting the the information from the response...')
        spotify_track = _extract_track_info_from_response(track_info_from_response, include_album, include_artists)

        return spotify_track


def _extract_track_info_from_response(track_info_from_response: dict,
                                      include_album: bool = True,
                                      include_artists: bool = True) -> SpotifyTrack:
    """Extract the track information from the Spotify's API response.

    Args:
        track_info_from_response (dict): the response section that includes the track information
        include_album (bool): if returned, populate the artists information in the returned SpotifyTrack,
                defaults to True
        include_artists (bool): if returned, populate the album information in the returned SpotifyTrack,
                defaults to True

    Returns: a SpotifyTrack instance
    """
    # If album needs to be included, check if it exists in the response and get the info
    if include_album and (album_info := track_info_from_response.get("album")):
        if ((release_date := album_info.get("release_date"))
                and (release_precision := album_info.get("release_date_precision"))):
            album_release_date = SpotifyAlbumReleaseDate(released_on=release_date, precision=release_precision)
        else:
            album_release_date = None

        spotify_album = SpotifyAlbum(album_info.get("name"), album_info.get("id"),
                                     album_type=album_info.get("type"), release_date=album_release_date,
                                     total_tracks=album_info.get("total_tracks"))
    else:
        spotify_album = None

    # If artists need to be included, check if they exist in the response and get the info
    if include_artists and (artists_info := track_info_from_response.get("artists")):
        spotify_artists = []
        for artist in artists_info:
            spotify_artists.append(SpotifyArtist(artist.get("name"), artist.get("id")))
    else:
        spotify_artists = None

    # Create and return the track
    spotify_track = SpotifyTrack(track_info_from_response.get("name"), track_info_from_response.get("id"),
                                 popularity=track_info_from_response.get("popularity"),
                                 duration=track_info_from_response.get("duration_in_ms"),
                                 explicit=track_info_from_response.get("explicit"),
                                 album=spotify_album, artists=spotify_artists)
    logging.info(f"Finished extracting track data for {spotify_track.name} ({spotify_track.track_id})")

    return spotify_track




if __name__ == '__main__':
    spotify_client = SpotifyClient('fe96fe66ef674b80b924b13faa97e627', '924fdbb9ef7c4df0bb6432d6fd619bdb')

    track = spotify_client.search_track('la bebé')
    print(track)
    print(str(track))
    print(repr(track))

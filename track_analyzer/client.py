import logging
import os
from typing import Optional

from .auth import SpotifyAuth
from .exceptions import SpotifyInvalidContentError, SpotifyException
from .spotify_album import SpotifyAlbum, SpotifyAlbumReleaseDate
from .spotify_artist import SpotifyArtist
from .spotify_audio_features import SpotifyAudioFeatures
from .spotify_track import SpotifyTrack
from .utils import make_http_request

DEFAULT_MARKET: str = os.environ.get('DEFAULT_MARKET', 'GT')  # Default the market to Guatemala

# Spotify's object types:
TRACK: str = "track"

# Spotify's paths:
SEARCH: str = "search"
AUDIO_FEATURES: str = "audio-features"


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
                     include_album: bool = True,
                     include_audio_features: bool = True) -> Optional[SpotifyTrack]:
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
            include_audio_features (bool): if returned, populate the audio features information in the returned
                SpotifyTrack, defaults to True

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

        if include_audio_features:
            if spotify_audio_features := self._get_audio_features(spotify_track):
                spotify_track.audio_features = spotify_audio_features
            else:
                logging.warning('Audio features were requested to be included in the track but they could not be '
                                'fetched.')

        return spotify_track

    def _get_audio_features(self, track: SpotifyTrack) -> Optional[SpotifyAudioFeatures]:
        """Retrieve the audio features for the given track

        Args:
            track (SpotifyTrack): the track that needs its audio features fetched

        Returns: a SpotifyAudioFeatures instance
        """
        path = f"{AUDIO_FEATURES}/{track.track_id}"
        # Make the HTTP request
        try:
            result = make_http_request(self.base_url, path, self._auth.access_token)

            # Create and return the audio features
            return SpotifyAudioFeatures(danceability=result.get("danceability"), energy=result.get("energy"),
                                        loudness=result.get("loudness"), mode=result.get("mode"),
                                        speechiness=result.get("speechiness"), tempo=result.get("tempo"),
                                        acousticness=result.get("acousticness"),
                                        instrumentalness=result.get("instrumentalness"),
                                        liveness=result.get("liveness"), valence=result.get("valence"))
        except SpotifyException as e:
            logging.warning(
                f"An error has occurred while trying to get the audio features for the {track.track_id} track. {e}")
            return None


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
                                 duration=track_info_from_response.get("duration_ms"),
                                 explicit=track_info_from_response.get("explicit"),
                                 album=spotify_album, artists=spotify_artists)
    logging.info(f"Finished extracting track data for {spotify_track.name} ({spotify_track.track_id})")

    return spotify_track


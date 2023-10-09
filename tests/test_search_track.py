from unittest import TestCase, main, mock
from unittest.mock import MagicMock

import requests

from misc.utils import mocked_search_track_response
from track_analyzer.client import SpotifyClient
from track_analyzer.exceptions import SpotifyInvalidContentError
from track_analyzer.spotify_album import SpotifyAlbum, SpotifyAlbumReleaseDate
from track_analyzer.spotify_artist import SpotifyArtist
from track_analyzer.spotify_track import SpotifyTrack


@mock.patch('track_analyzer.auth.SpotifyAuth.access_token', return_value='my_access_token')
@mock.patch('track_analyzer.utils.requests.get')
class TestSearchTrack(TestCase):
    """This class contains a collection of different test cases related to the search functionality

    The following patches are applied at class level:
    * SpotifyAuth->access_token: a generic "my_access_token" is set as the access token
    * requests->get: all the GET requests to the Spotify API will be mocked out
    """

    def setUp(self):
        """Setup common values
        """
        client_id = 'my_client_id'
        client_secret = 'my_client_secret'
        self.spotify_client = SpotifyClient(client_id, client_secret)

    def test_search_track(self, mock_requests_get, mock_access_token):
        """Test the search track function returns a valid SpotifyTrack instance if the response from the Spotify API
        is successful
        """
        # Mock the request to the Spotify API
        mock_requests_get.return_value.status_code = requests.codes.ok
        mock_requests_get.return_value.json = MagicMock(return_value=mocked_search_track_response())

        # Search for a track
        spotify_track = self.spotify_client.search_track('search for a track')

        # Assert the data is correct
        self.assertIsInstance(spotify_track, SpotifyTrack)
        self.assertIsInstance(spotify_track.name, str)
        self.assertIsInstance(spotify_track.track_id, str)
        self.assertIsInstance(spotify_track.duration, int)
        self.assertIsInstance(spotify_track.human_duration, str)
        # Match from 1 to 5 min, seconds from 00 (always including a leading zero) to 59
        self.assertRegex(spotify_track.human_duration, r'^[1-5]:(0[0-9]|[1-5][0-9])$')
        # Popularity must be between 0 and 100
        self.assertTrue(0 <= spotify_track.popularity <= 100)

        # Check the album...
        self.assertIsInstance(spotify_track.album, SpotifyAlbum)
        self.assertIsInstance(spotify_track.album.name, str)
        self.assertIsInstance(spotify_track.album.album_id, str)
        self.assertIsInstance(spotify_track.album.release_date, SpotifyAlbumReleaseDate)
        # ...and the artists
        self.assertIsInstance(spotify_track.artists, list)
        for artist in spotify_track.artists:
            self.assertIsInstance(artist, SpotifyArtist)
            self.assertIsInstance(artist.name, str)
            self.assertIsInstance(artist.artist_id, str)

    def test_search_track_not_found(self, mock_requests_get, mock_access_token):
        """Test the search track function returns None if no matching track was found
        """
        # Mock the request to the Spotify API
        mock_requests_get.return_value.status_code = requests.codes.ok
        mock_requests_get.return_value.json = MagicMock(return_value=mocked_search_track_response(no_match=True))

        # Search for a track
        spotify_track = self.spotify_client.search_track('search for a track')

        # Assert the return value is None
        self.assertIsNone(spotify_track)

    def test_search_track_invalid_response(self, mock_requests_get, mock_access_token):
        """Test the search track function raises an error if the response from the Spotify API contains invalid data
        """
        # Mock the request to the Spotify API
        mock_requests_get.return_value.status_code = requests.codes.ok
        mock_requests_get.return_value.json = MagicMock(return_value={"message": "This is an invalid response!"})

        with self.assertRaises(SpotifyInvalidContentError):
            self.spotify_client.search_track('search for a track')


if __name__ == '__main__':
    main()

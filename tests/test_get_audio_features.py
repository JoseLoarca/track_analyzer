from unittest import TestCase, main, mock
from unittest.mock import MagicMock

import requests

from track_analyzer.client import SpotifyClient
from track_analyzer.exceptions import SpotifyLimitExceededError
from track_analyzer.spotify_audio_features import SpotifyAudioFeatures
from track_analyzer.spotify_track import SpotifyTrack


@mock.patch('track_analyzer.auth.SpotifyAuth.access_token', return_value='my_access_token')
@mock.patch('track_analyzer.utils.requests.get')
class TestGetAudioFeatures(TestCase):
    """This class contains a collection of test cases related to the _get_audio_features method

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

    def test_get_audio_features(self, mock_requests_get, mock_access_token):
        """Test the audio features are correctly obtained when the Spotify API returns a successful response
        """
        # These are the real audio features for Moby's Porcelain obtained from the Spotify API
        audio_features_dict = {
            "danceability": 0.515,
            "energy": 0.613,
            "loudness": -8.423,
            "mode": 0,
            "speechiness": 0.0305,
            "acousticness": 0.00147,
            "instrumentalness": 0.202,
            "liveness": 0.449,
            "valence": 0.357,
            "tempo": 94.925
        }
        # Mock the request to the Spotify API
        mock_requests_get.return_value.status_code = requests.codes.ok
        mock_requests_get.return_value.json = MagicMock(return_value=audio_features_dict)

        spotify_track = SpotifyTrack("Porcelain", "1hEh8Hc9lBAFWUghHBsCel")
        audio_features = self.spotify_client._get_audio_features(spotify_track)

        # Assert data was fetched correctly
        self.assertIsInstance(audio_features, SpotifyAudioFeatures)
        for key, value in audio_features_dict.items():
            self.assertEqual(getattr(audio_features, key), value)

    def test_get_audio_features_failed_request(self, mock_requests_get, mock_access_token):
        """Test the _get_audio_features method returns None if the audio_features can not be obtained due to errors
        from the Spotify API
        """
        # Mock the request to the Spotify API
        mock_requests_get.side_effect = SpotifyLimitExceededError
        spotify_track = SpotifyTrack("One of These Mornings", "1PfghsEk6A9RdLCRT5tlIV")

        with self.assertLogs() as log:  # Assert a log message was generated
            audio_features = self.spotify_client._get_audio_features(spotify_track)
            self.assertIsNone(audio_features)  # The return value should be none
            self.assertIn("An error has occurred while trying to get the audio features", log.output[0])


if __name__ == '__main__':
    main()

from unittest import mock, TestCase, main
from requests import codes

from track_analyzer.auth import SpotifyAuth
from track_analyzer.exceptions import SpotifyAuthenticationError


@mock.patch('track_analyzer.auth.requests.post')  # Mock at class level as all the tests will use it
class TestAuth(TestCase):
    """This class contains a collection of different test cases related to authentication to the Spotify API
    """

    def setUp(self):
        """Setup common variables
        """
        self.spotify_auth = SpotifyAuth('my_client_id', 'my_client_secret')

    def test_generate_access_token(self, mock_requests_post):
        """Make sure a token is generated when the Spotify API returns a valid access_token
        """
        # Mock the return value of requests' post
        mock_requests_post.return_value.status_code = codes.ok
        mock_requests_post.return_value.json.return_value = {"access_token": "spotify_access_token", "expires_in": 3600}

        # Assert the token was generated successfully
        self.assertEqual(self.spotify_auth.access_token, "spotify_access_token")

    def test_generate_access_token_fails(self, mock_requests_post):
        """Make sure a SpotifyAuthenticationError exception is raised if the Spotify API doesn't return a valid response
        """
        # Mock the return value of requests' post
        mock_requests_post.return_value.status_code = codes.too_many_requests
        mock_requests_post.return_value.json.return_value = {"error": "Too many requests."}

        # Assert SpotifyAuthenticationError is raised and an error message is logged
        with self.assertRaises(SpotifyAuthenticationError), self.assertLogs() as log:
            # Calling _generate_access_token will raise an exception and log an error message
            self.spotify_auth._generate_access_token()

            # Assert the logged message is what we are expecting
            self.assertEqual(len(log.output), 1)
            self.assertIn(f"Could not generate access token. Status code: {codes.too_many_requests}",
                          log.output[0])

    def test_access_token_is_generated_when_no_token(self, mock_requests_post):
        """Make sure a new access token is generated if the SpotifyAuth object doesn't already contain one
        """
        # Mock the return value of requests' post
        mock_requests_post.return_value.status_code = codes.ok
        mock_requests_post.return_value.json.return_value = {"access_token": "spotify_access_token", "expires_in": 3600}

        # Trigger the generation of the token
        self.assertEqual(self.spotify_auth.access_token, "spotify_access_token")

        # Since the SpotifyAuth object did not already contain a valid token,
        # we make sure a request to obtain a new access token was made
        body = {"grant_type": "client_credentials", "client_id": 'my_client_id', "client_secret": 'my_client_secret'}
        auth_url = 'https://accounts.spotify.com/api/token'
        mock_requests_post.assert_called_once_with(auth_url, data=body)


if __name__ == '__main__':
    main()

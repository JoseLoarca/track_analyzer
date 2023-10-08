from unittest import TestCase, main, mock

from requests import codes, RequestException, ConnectionError

from track_analyzer.utils import make_http_request
from track_analyzer.exceptions import (SpotifyUnauthorizedError,
                                       SpotifyForbiddenOperationError,
                                       SpotifyLimitExceededError,
                                       SpotifyUnknownStatusError)


@mock.patch('track_analyzer.utils.requests.get')  # Mock at class level as all the tests will use it
class TestMakeHttpRequest(TestCase):
    """This class contains a collection of different test cases related to making HTTP requests
    """

    def test_successful_request(self, mock_requests_get):
        """Make sure a dict is returned when a successful response is received
        """
        # Mock the successful response
        response = {"message": "it works!"}
        mock_requests_get.return_value.status_code = codes.ok
        mock_requests_get.return_value.json.return_value = response

        result = make_http_request(base_url="https://api.spotify.com/v1",
                                   path="search",
                                   access_token="spotify_access_token",
                                   query_params={"foo": "bar"})

        # Assert the return value is a dict that matches the mocked return value
        self.assertIsInstance(result, dict)
        self.assertEqual(result, response)

    def test_unauthorized_request(self, mock_requests_get):
        """Make a SpotifyUnauthorizedError is raised when a 401 status is returned by the Spotify API
        """
        # Mock the unauthorized request
        mock_requests_get.return_value.status_code = codes.unauthorized

        # Assert SpotifyUnauthorizedError is raised
        with self.assertRaises(SpotifyUnauthorizedError):
            make_http_request(base_url="https://api.spotify.com/v1",
                              path="search",
                              access_token="spotify_access_token",
                              query_params={"foo": "bar"})

    def test_forbidden_request(self, mock_requests_get):
        """Make a SpotifyForbiddenOperationError is raised when a 403 status is returned by the Spotify API
        """
        # Mock the forbidden request
        mock_requests_get.return_value.status_code = codes.forbidden

        # Assert SpotifyUnauthorizedError is raised
        with self.assertRaises(SpotifyForbiddenOperationError):
            make_http_request(base_url="https://api.spotify.com/v1",
                              path="search",
                              access_token="spotify_access_token",
                              query_params={"foo": "bar"})

    def test_limit_exceeded_request(self, mock_requests_get):
        """Make a SpotifyLimitExceededError is raised when a 429 status is returned by the Spotify API
        """
        # Mock the rate limit exceeded request
        mock_requests_get.return_value.status_code = codes.too_many_requests

        # Assert SpotifyUnauthorizedError is raised
        with self.assertRaises(SpotifyLimitExceededError):
            make_http_request(base_url="https://api.spotify.com/v1",
                              path="search",
                              access_token="spotify_access_token",
                              query_params={"foo": "bar"})

    def test_unknown_status_request(self, mock_requests_get):
        """Make a SpotifyUnknownStatusError is raised when an unknown status is returned by the Spotify API
        """
        # Mock the unknown status request
        mock_requests_get.return_value.status_code = codes.bad_request

        # Assert SpotifyUnauthorizedError is raised
        with self.assertRaises(SpotifyUnknownStatusError):
            make_http_request(base_url="https://api.spotify.com/v1",
                              path="search",
                              access_token="spotify_access_token",
                              query_params={"foo": "bar"})

    def test_failed_request(self, mock_requests_get):
        """Make a RequestException is raised when an HTTP request fails
        """
        # Mock the unauthorized request
        mock_requests_get.side_effect = ConnectionError

        # Assert RequestException is raised
        with self.assertRaises(RequestException):
            make_http_request(base_url="https://api.spotify.com/v1",
                              path="search",
                              access_token="spotify_access_token",
                              query_params={"foo": "bar"})


if __name__ == '__main__':
    main()

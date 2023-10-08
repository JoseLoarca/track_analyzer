from unittest import TestCase, main

from track_analyzer.spotify_album import SpotifyAlbum


class TestSpotifyAlbum(TestCase):
    """This class contains a collection of different test cases related to the SpotifyAlbum class
    """

    def test_spotify_album_constructor(self):
        """Test the creation of a SpotifyAlbum instance with the basic data is successful
        """
        name = "my_album"
        album_id = "abc123abc123"
        # Create a new SpotifyAlbum instance
        my_album = SpotifyAlbum(name, album_id)

        # Assert the result contains valid data
        self.assertIsInstance(my_album, SpotifyAlbum)
        self.assertEqual(my_album.name, name)
        self.assertEqual(my_album.album_id, album_id)

    def test_spotify_album_constructor_validation(self):
        """Test the constructor raises ValueError errors if invalid data is passed
        """
        with self.assertRaises(ValueError):  # Popularity must be between 0 and 100
            SpotifyAlbum("My super popular album", "album_id", popularity=1000)

        with self.assertRaises(ValueError):  # Album type must be an allowed type (single, album, compilation)
            SpotifyAlbum("My unreleased album", "album_id", album_type="unreleased")


if __name__ == '__main__':
    main()

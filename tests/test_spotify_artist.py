from unittest import TestCase, main

from track_analyzer.spotify_artist import SpotifyArtist


class TestSpotifyArtist(TestCase):
    """This class contains a collection of different test cases related to the SpotifyArtist class
    """

    def test_spotify_artist_constructor(self):
        """Test the creation of a SpotifyArtist instance with the basic data is successful
        """
        name = "John Doe"
        artist_id = "abc123abc123"
        # Create a new SpotifyArtist instance
        my_artist = SpotifyArtist(name, artist_id)

        # Assert the result contains valid data
        self.assertIsInstance(my_artist, SpotifyArtist)
        self.assertEqual(my_artist.name, name)
        self.assertEqual(my_artist.artist_id, artist_id)

    def test_spotify_artist_constructor_validation(self):
        """Test the constructor raises ValueError errors if invalid data is passed
        """
        with self.assertRaises(ValueError):  # Popularity must be between 0 and 100
            SpotifyArtist("Fulano", "artist_id", popularity=-100)


if __name__ == '__main__':
    main()

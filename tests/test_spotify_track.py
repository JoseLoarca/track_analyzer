from unittest import TestCase, main

from track_analyzer.spotify_track import SpotifyTrack


class TestSpotifyTrack(TestCase):
    """This class contains a collection of different test cases related to the SpotifyArtist class
    """

    def test_spotify_track_constructor(self):
        """Test the creation of a SpotifyTrack instance with the basic data is successful
        """
        name = "My Track"
        track_id = "abc123abc123"
        # Create a new SpotifyArtist instance
        my_track = SpotifyTrack(name, track_id)

        # Assert the result contains valid data
        self.assertIsInstance(my_track, SpotifyTrack)
        self.assertEqual(my_track.name, name)
        self.assertEqual(my_track.track_id, track_id)

    def test_spotify_track_constructor_validation(self):
        """Test the constructor raises ValueError errors if invalid data is passed
        """
        with self.assertRaises(ValueError):  # Popularity must be between 0 and 100
            SpotifyTrack("My amazing track!!", "track_id", popularity=9999)

    def test_spotify_track_is_explicit(self):
        """Test the is_explicit property method returns the right value
        """
        unknown_explicit_track = SpotifyTrack("I don't know if this track is explicit", "unknown")
        # The default value for the "explicit" flag is None
        self.assertIsNone(unknown_explicit_track.is_explicit)

        explicit_track = SpotifyTrack("This is not for kids!", "explicit", explicit=True)
        # An explicit track should return True
        self.assertTrue(explicit_track.is_explicit)

        not_explicit_track = SpotifyTrack("Bring the whole family!", "not_explicit", explicit=False)
        # A not explicit track should return False
        self.assertFalse(not_explicit_track.is_explicit)

    def test_spotify_track_human_duration(self):
        """Test the human_duration property method returns the right value
        """
        dia_especial = SpotifyTrack("Dia Especial", "1XyRT1VeLaJs5rEJA3rMO9", duration=262666)
        # Shakira's Día Especial is 4 minutes and 22 seconds long
        self.assertEqual(dia_especial.human_duration, "4:22")


if __name__ == '__main__':
    main()

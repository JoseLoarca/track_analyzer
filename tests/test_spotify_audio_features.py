from unittest import TestCase, main

from track_analyzer.spotify_audio_features import SpotifyAudioFeatures


class TestSpotifyAudioFeatures(TestCase):
    """This class contains a collection of different test cases related to the SpotifyAudioFeatures class
        """

    def test_spotify_audio_features_constructor(self):
        """Test the creation of a SpotifyAudioFeatures instance is successful
        """
        acousticness = 0.963
        mode = 1
        tempo = 109.619
        audio_features = SpotifyAudioFeatures(acousticness=acousticness, mode=mode, tempo=tempo)

        # Assert the returned data is correct
        self.assertIsInstance(audio_features, SpotifyAudioFeatures)
        self.assertEqual(audio_features.acousticness, acousticness)
        self.assertEqual(audio_features.mode, mode)
        self.assertEqual(audio_features.tempo, tempo)

    def test_spotify_audio_features_constructor_validation(self):
        """Test the constructor raises ValueError errors if invalid data is passed
        """
        with self.assertRaises(ValueError):  # The acousticness must be between 0 and 1
            SpotifyAudioFeatures(acousticness=1.1)

        with self.assertRaises(ValueError):  # The danceability must be between
            SpotifyAudioFeatures(danceability=10)

        with self.assertRaises(ValueError):  # The modality should be either 0 or 1
            SpotifyAudioFeatures(mode=2)


if __name__ == '__main__':
    main()

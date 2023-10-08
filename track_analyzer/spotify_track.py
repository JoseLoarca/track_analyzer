from typing import Optional

from .spotify_audio_features import SpotifyAudioFeatures


class SpotifyTrack:
    """This class represents a Spotify track
    """

    def __init__(self,
                 name: str,
                 track_id: str,
                 *,

                 popularity: Optional[int] = None,
                 duration: Optional[int] = None,
                 audio_features: Optional[SpotifyAudioFeatures] = None,
                 explicit: Optional[bool] = None):
        """Create a new SpotifyTrack instance

        Args:
            name (str): the name of the song
            track_id (str): the Spotify ID of the track
            -
             popularity (Optional[int]): the popularity of the track, this should be a value from 0 to 100,
                with 100 being the most popular
            duration (Optional[int]): the duration of the track in milliseconds
            audio_features (Optional[SpotifyAudioFeatures]): the audio features for the track
            explicit (Optional[bool]): indicates if the track is explicit or not
        """
        # If provided, make sure popularity is between 0 and 100
        if popularity is not None and not (0 <= popularity <= 100):
            raise ValueError("The popularity of the artist should be between 0 and 100.")

        self.name = name
        self.track_id = track_id
        # Keyword args
        self.popularity = popularity
        self.duration = duration
        self.audio_features = audio_features
        self._explicit = explicit

    @property
    def is_explicit(self) -> Optional[bool]:
        """Returns if the track is explicit or not

        Returns: a bool that indicates if the track is explicit or not. If the flag is not set, this will return None
        """
        if self._explicit is not None:
            return self._explicit

    @property
    def human_duration(self) -> Optional[str]:
        """Returns the duration of the track a human friendly format: min:sec.
        This is done by:
        1. Converting the duration (milliseconds) to seconds
        2. Get the minutes by doing integer division
        3. Get the seconds by doing a mod operation (remainder)

        The seconds section of the returned value will always include leading zero, so for a track that is 2 minutes and
        1 seconds, the return value would be: 2:01

        Returns: the duration of the track in a human friendly format: min:sec. If the duration is not set, this will
        return None

        Examples:
            216133 -> 3:36 (3 minutes and 36 seconds)
        """
        if self.duration:
            duration_in_seconds = self.duration / 1000
            minutes = int(duration_in_seconds // 60)  # Integer division to get the minutes
            seconds = int(duration_in_seconds % 60)  # Mod operation to get the seconds

            return f"{minutes}:{seconds:02d}"

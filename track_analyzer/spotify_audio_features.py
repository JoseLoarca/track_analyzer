from typing import Optional


class SpotifyAudioFeatures:
    """This class represents a Spotify track's audio feature
    """

    def __init__(self,
                 *,
                 acousticness: float = 0.0,
                 danceability: float = 0.0,
                 energy: float = 0.0,
                 instrumentalness: float = 0.0,
                 liveness: float = 0.0,
                 loudness: float = 0.0,
                 mode: Optional[int] = None,
                 speechiness: float = 0.0,
                 tempo: float = 0.0,
                 valence: float = 0.0
                 ):
        """Create a new instance of SpotifyAudioFeatures

        Args:
            acousticness (float): a confidence measure from 0.0 to 1.0 of whether the track is acoustic.
                1.0 represents high confidence the track is acoustic.
            danceability (float): describes how suitable a track is for dancing. A value of 0.0 is least danceable
                and 1.0 is most danceable.
            energy (float): the energy is measured from 0.0 to 1.0 and represents a perceptual measure of intensity
                and activity
            instrumentalness (float): predicts whether a track contains no vocals. The closer this value is to 1.0,
                the greater likelihood the track contains no vocal content.
            liveness (float): detects the presence of an audience in the recording. Higher liveness values represent an
                increased probability that the track was performed live. A value above 0.8 provides strong
                likelihood that the track is live.
            mode (Optional[int]): indicates the modality (major or minor) of a track, the type of scale from which its
                melodic content is derived. Major is represented by 1 and minor is 0.
            speechiness (float): detects the presence of spoken words in a track. The more exclusively speech-like
                the recording (e.g. talk show, audiobook, poetry), the closer to 1.0
            tempo (float): the overall estimated tempo of a track in beats per minute (BPM)
            valence (float): a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.
                Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),
                while tracks with low valence sound more negative (e.g. sad, depressed, angry).


        The explanation for all these fields was obtained from the Spotify's developer dashboard, see:
        https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
        """
        # The following fields must be between 0.0 and 1.0. If provided, we want to make sure they contain a valid value
        common_validation_fields = {"acousticness": acousticness, "danceability": danceability, "energy": energy,
                                    "valence": valence}

        for field, value in common_validation_fields.items():
            if value is not None and not (0.0 <= value <= 1.0):
                raise ValueError(f"The {field} of the track should be between 0.0 and 1.0.")

        # If provided, make sure the modality of the track contains a valid value (0 or 1)
        if mode is not None and mode not in (0, 1):
            raise ValueError("The modality of the track should can only be 0 or 1.")

        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.valence = valence

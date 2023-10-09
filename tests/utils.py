from faker import Faker

faker = Faker()


def mocked_search_track_response(no_match: bool = False) -> dict:
    """Mock the response for the search operation from the Spotify API

    Args:
        no_match (bool): indicates if an empty response should be returned

    Returns: a dict containing the mocked response

    The response from Spotify, when a matching track is found, contains a JSON like the following:

    {
    "tracks": {
        "href": "string:url",
        "items": [
            {
                "album": {
                    "album_type": "string",
                    "artists": [
                        {
                            "external_urls": {
                                "spotify": "string:url"
                            },
                            "href": "string:url",
                            "id": "string",
                            "name": "string",
                            "type": "string",
                            "uri": "string:uri"
                        }
                    ],
                    "external_urls": {
                        "spotify": "string:url"
                    },
                    "href": "string:url",
                    "id": "string",
                    "images": [
                        {
                            "height": int,
                            "url": "string:url",
                            "width": int
                        },
                        {
                            "height": int,
                            "url": "string:url",
                            "width": int
                        },
                        {
                            "height": int,
                            "url": "string:url",
                            "width": int
                        }
                    ],
                    "is_playable": bool,
                    "name": "string",
                    "release_date": "string:date-like",
                    "release_date_precision": "string",
                    "total_tracks": int,
                    "type": "string",
                    "uri": "string:uri"
                },
                "artists": [
                    {
                        "external_urls": {
                            "spotify": "string:url"
                        },
                        "href": "string:url",
                        "id": "string",
                        "name": "string",
                        "type": "string",
                        "uri": "string:uri"
                    }
                ],
                "disc_number": int,
                "duration_ms": int,
                "explicit": false,
                "external_ids": {
                    "isrc": "string"
                },
                "external_urls": {
                    "spotify": "string:url"
                },
                "href": "string:url",
                "id": "string",
                "is_local": bool,
                "is_playable": bool,
                "name": "string",
                "popularity": int,
                "preview_url": "string:url",
                "track_number": int,
                "type": "string",
                "uri": "string:uri"
            }
        ],
        "limit": int,
        "next": "string:url",
        "offset": int,
        "previous": "string:url:nullable",
        "total": int
        }
    }

    Note: in order to keep things simple, some sections that are not currently in use will not be returned
    """
    if no_match:
        # Response for no matching track found, the empty "items" field indicates no matching tracks were found
        return {
            "tracks": {
                "href": "https://api.spotify.com/v1",
                "items": [],
                "limit": 1,
                "next": "https://api.spotify.com/v1",
                "offset": 0,
                "previous": None,
                "total": 0
            }
        }

    return {
        "tracks": {
            "href": "https://api.spotify.com/v1",
            "items": [
                {
                    "album": {
                        "album_type": faker.random_element(elements=('single', 'album', 'compilation')),
                        "id": faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9'),
                        "is_playable": faker.boolean(),
                        "name": faker.text(max_nb_chars=20),
                        "release_date": faker.date(),
                        "release_date_precision": "day",
                        "total_tracks": 1,
                        "type": "album",
                        "uri": "spotify:album" + faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9')
                    },
                    "artists": [
                        {
                            "id": faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9'),
                            "name": faker.name(),
                            "type": "artist",
                            "uri": "spotify:artist:" + faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9')
                        }
                    ],
                    "disc_number": 1,
                    "duration_ms": faker.random_int(min=60000, max=300000),
                    "explicit": faker.boolean(),
                    "id": faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9'),
                    "is_local": faker.boolean(),
                    "is_playable": faker.boolean(),
                    "name": faker.text(max_nb_chars=20),
                    "popularity": faker.random_int(min=0, max=100),
                    "preview_url": "https://api.spotify.com/v1",
                    "track_number": 1,
                    "type": "track",
                    "uri": "spotify:track:" + faker.pystr(min_chars=10, max_chars=10, prefix='1', suffix='9')
                }
            ],
            "limit": 1,
            "next": "https://api.spotify.com/v1",
            "offset": 0,
            "previous": None,
            "total": 1
        }
    }

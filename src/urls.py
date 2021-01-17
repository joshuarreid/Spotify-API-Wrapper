"""Library for containing Spotify Web API Urls.
"""

class URLs:
    """
    The URLs class is responsible for containing URL strings and serving them to the API Wrapper.
    """
    def __init__(self, response_format='json'):
        self.format = response_format
        self.base_url = 'https://api.spotify.com/v1/'
        self.authUrl = "https://accounts.spotify.com/api/token"

        # Albums
        self.albums = 'albums/{id}'.format(format=self.format, id='{id}')
        self.albumTracks = 'albums/{id}/tracks'.format(format=self.format, id='{id}')

        # Tracks
        self.tracks = 'tracks/{id}'.format(format=self.format, id='{id}')
        self.track_audio_features = 'audio-features/{id}'.format(format=self.format, id='{id}')

        # Artists
        self.artists = 'artists/{id}'.format(format=self.format, id='{id}')
        self.artists_albums = 'artists/{id}/albums'.format(format=self.format, id='{id}')
        self.artists_top_tracks = 'artists/{id}/albums/top-tracks'.format(format=self.format, id='{id}')
        self.artists_related = 'artists/{id}/albums/related-artists'.format(format=self.format, id='{id}')



    def base_url(self):
        return self.base_url



    def albums_url(self):
        return self.base_url + self.albums



    def albums_tracks_url(self):
        return self.base_url + self.albumTracks



    def tracks_url(self):
        return self.base_url + self.tracks



    def tracks_audio_features_url(self):
        return self.base_url + self.track_audio_features



    def artists_url(self):
        return self.base_url + self.artists



    def artists_albums_url(self):
        return self.base_url + self.artists_albums



    def artists_top_tracks_url(self):
        return self.base_url + self.artists_top_tracks



    def artists_related_url(self):
        return self.base_url + self.artists_related
import requests
import base64, json
from src.artist import Artist
from src.URLs import URLs
from src.track import Track


class SpotifyAPI:
    def __init__(self, clientID, clientSecret, response_format='json'):
        self.format = response_format
        self.url = URLs(response_format=response_format)

        self.clientID = clientID
        self.clientSecret = clientSecret



    def __create_access_Token(self):
        """
        This method creates an access token to make calls to the Spotify API

        :return: None
        """
        authHeader = {}
        authData = {}
        # Encoding clientID and clientSecret in base64
        message = f"{self.clientID}:{self.clientSecret}"
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        authHeader['Authorization'] = "Basic " + base64_message
        authData['grant_type'] = 'client_credentials'
        response = requests.post(self.url.authUrl, headers=authHeader, data=authData)
        # request returns json
        responseObject = response.json()
        self.accessToken = responseObject['access_token']



    def __to_format(self, response):
        """
        This method formats Spotify API responses into a json

        :param response: A response from Spotify API
        :return: json
        """
        if self.format == 'json':
            return response.json()



    def __get_data(self, url, params=None):
        """

        :param url: the Spotify API call url
        :param params: {dict} parameters to include in API call
        :return: request.get formatted
        """
        self.__create_access_Token()
        getheader = {
            "Content-Type": "json",
            "Authorization": "Bearer " + self.accessToken
        }
        if params:
            return self.__to_format(requests.get(url, headers=getheader, params=params))
        else:
            return self.__to_format(requests.get(url, headers=getheader))



    def get_album(self, album_id):
        return self.__get_data(self.url.albums_url().format(id=str(album_id)))



    def get_album_tracks(self, album_id):
        return self.__get_data(self.url.albums_tracks_url().format(id=str(album_id)))



    def get_track(self, track_id):
        response = self.__get_data(self.url.tracks_url().format(id=str(track_id)))
        name = response['name']
        album = response['album']['name']
        album_id = response['album']['id']
        artists = []
        artists_id = []
        for artist in response['artists']:
            artists.append(artist['name'])
            artists_id.append(artist['id'])
        duration_ms = response['duration_ms']
        explicit = response['explicit']
        release_date = response['album']['release_date']
        popularity = response['popularity']
        return Track(name=name, album=album, artists=artists, popularity=popularity, track_id=track_id, album_id=album_id,
                     artists_id=artists_id, duration_ms=duration_ms, explicit=explicit, release_date=release_date)





    def get_track_audio_features(self, track_id):
        return self.__get_data(self.url.tracks_audio_features_url().format(id=str(track_id)))



    def get_artist_albums(self, artist_id):
        return self.__get_data(self.url.artists_albums_url().format(id=str(artist_id)))



    def get_artist_top_tracks(self, artists_id, country='US'):
        params = {
            "country": country
        }
        return self.__get_data(self.url.artists_top_tracks_url().format(id=str(artists_id)), params=params)



    def get_artist_related(self, artists_id):
        response = self.__get_data(self.url.artists_related_url().format(id=str(artists_id)))
        artists = []
        for related_artist in response['artists']:
            artist = Artist(artist_id=related_artist['id'], name=related_artist['name'], popularity=related_artist['popularity'], genres=related_artist['genres'])
            artists.append(artist)
        return artists




    def get_artist(self, artist_id):
        response = self.__get_data(self.url.artists_url().format(id=str(artist_id)))
        return Artist(artist_id=artist_id, name=response['name'], popularity=response['popularity'],
                        genres=response['genres'])


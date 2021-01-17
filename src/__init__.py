"""Library for making calls to the Spotify Web API.

    Get information on artists, albums, tracks, and more. This module provides an easy
    way to fetch spotify information and organizes them in functional objects.

    Some Available methods:
    - get_album: Gets album information
    - get_track: Gets track information
    - get_artist: Gets artist information


"""

import base64

import requests

from src.URLs import URLs
from src.artist import Artist
from src.track import Track


class SpotifyAPI:
    """ Represents a session with the Spotify Web API """



    def __init__(self, clientID, clientSecret, response_format='json'):
        """ Initializes session with Spotify Web API.

            :param clientID: String of the Client ID provided by Developer.Spotify.com
            :param clientSecret: String of the Client Secret provided by Developer.Spotify.com
            :param response_format: String of the response format
        """
        self.format = response_format
        self.url = URLs(response_format=response_format)

        self.clientID = clientID
        self.clientSecret = clientSecret



    def __create_access_token(self):
        """ This method creates an Access Token to make calls to the Spotify Web API.

            This method combines the Client ID and Client Secret Strings and encodes them
            in base64. After combining the two Strngs , it makes a post to the Spotify Auth. URL,
            which returns a dictionary containing the access token. This is stored in the public
            attribute access_token.
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
        self.access_token = responseObject['access_token']



    def __to_format(self, response):
        """This method formats a Spotify Web API response into a json.

            :param response: A response from Spotify Web API
            :return: json
        """
        if self.format == 'json':
            return response.json()



    def __get_data(self, url, params=None):
        """This method is responsible for making a get request to the Spotify Web API.

            This method creates a formatted header for the get request to the Spotify Web API.
            It also can provide parameters in the call if needed. The method calls the __create_access_token
            method everytime it is called.

            :param url: the String of the Spotify Web API call url
            :param params: the dictionary containing the parameters to include in API call
            :return: a json of the response from the Spotify Web API
        """
        self.__create_access_token()
        getheader = {
            "Content-Type": "json",
            "Authorization": "Bearer " + self.access_token
        }
        if params:
            return self.__to_format(requests.get(url, headers=getheader, params=params))
        else:
            return self.__to_format(requests.get(url, headers=getheader))



    def get_album(self, album_id):  # TODO return an Album object
        """ This method fetches album information from a Spotify album ID.

            This method makes a call to the Spotify Web API and returns the information in
            an Album object containing the information about the album. An album ID can be
            found in the Spotify link to the album: https://open.spotify.com/album/{album_id}.

            :param album_id: A String of the album ID
            :return: An Album object
        """
        return self.__get_data(self.url.albums_url().format(id=str(album_id)))



    def get_album_tracks(self, album_id):  # TODO return a list of Track objects
        """ This method returns a list of Track objects from a Spotify album ID.

            :param album_id: A String of the album ID
            :return: A list of Track objects
        """
        return self.__get_data(self.url.albums_tracks_url().format(id=str(album_id)))



    def get_track(self, track_id):
        """ This method fetches track information from a Spotify track ID.

            This method makes a call to the Spotify Web API and returns the information in
            a Track object containing the information about the track. A songs track ID can be
            found in the Spotify link to the track: https://open.spotify.com/track/{track_id}.

            :param track_id: A String of the track ID
            :return: A Track object
        """
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
        return Track(name=name, album=album, artists=artists, popularity=popularity, track_id=track_id,
                     album_id=album_id,
                     artists_id=artists_id, duration_ms=duration_ms, explicit=explicit, release_date=release_date)



    def get_track_audio_features(self, track_id):  # TODO initialize and return a subclass object of Track
        """This method fetches audio information for a track from a Spotify track ID

            :param track_id: A String of the track ID
            :return: A subclass of a Track object
        """
        return self.__get_data(self.url.tracks_audio_features_url().format(id=str(track_id)))



    def get_artist(self, artist_id):
        """ This method fetches artist information from a Spotify artist ID.

            This method makes a call to the Spotify Web API and returns the information in
            an Artist object containing the information about the artist. An artist ID can be
            found in the Spotify link to the artist: https://open.spotify.com/artist/{artist_id}.

            :param artist_id: A String of the artist ID
            :return: An Artist object
        """
        response = self.__get_data(self.url.artists_url().format(id=str(artist_id)))
        return Artist(artist_id=artist_id, name=response['name'], popularity=response['popularity'],
                      genres=response['genres'])



    def get_artist_albums(self, artist_id):  # TODO initialize and return a list of Album objects
        """ This method fetches the albums of an artist.

            :param artist_id: A String of the artist ID
            :return: A list of Album objects
        """
        return self.__get_data(self.url.artists_albums_url().format(id=str(artist_id)))



    def get_artist_top_tracks(self, artists_id, country='US'):  # TODO initialize and return a list of Track objects
        """ This method fetches the top tracks of an artist.

            :param artists_id: A String of the artist ID
            :param country: A String of a countries abbreviation
            :return: A list of Track objects
        """
        params = {
            "country": country
        }
        return self.__get_data(self.url.artists_top_tracks_url().format(id=str(artists_id)), params=params)



    def get_artist_related(self, artists_id):
        """ This method fetches the related artists of an artist.

            :param artists_id: A String of the artist ID
            :return: A list of Artist objects
        """
        response = self.__get_data(self.url.artists_related_url().format(id=str(artists_id)))
        list_of_related_artists = []
        for related_artist in response['artists']:
            artist = Artist(artist_id=related_artist['id'], name=related_artist['name'],
                            popularity=related_artist['popularity'], genres=related_artist['genres'])
            list_of_related_artists.append(artist)
        return list_of_related_artists

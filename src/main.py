import requests
import secrets
import base64, json


# curl -X "POST" -H "Authorization: Basic ZjM4ZjAw...WY0MzE=" -d grant_type=client_credentials https://accounts.spotify.com/api/token

class URLs:
    """
    The urls class is responsible for holding URL strings and serving them to the API Wrapper
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
        self.artists_albums = self.artists + '/albums'
        self.artists_top_tracks = self.artists + '/top-tracks'
        self.artists_related = self.artists + '/related-artists'



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


class SpotifyAPI:
    def __init__(self, clientID, clientSecret, response_format='json'):
        self.format = response_format
        self.url = URLs(response_format=response_format)

        self.clientID = clientID
        self.clientSecret = clientSecret



    def __create_access_Token(self):
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
        if self.format == 'json':
            return response.json()



    def __get_data(self, url, params=None):
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
        return self.__get_data(self.url.tracks_url().format(id=str(track_id)))



    def get_track_audio_features(self, track_id):
        return self.__get_data(self.url.tracks_audio_features_url().format(id=str(track_id)))



    def get_artists_albums(self, artist_id):
        return self.__get_data(self.url.artists_albums_url().format(id=str(artist_id)))



    def get_artists_top_tracks(self, artists_id, country='US'):
        params = {
            "country": country
        }
        return self.__get_data(self.url.artists_top_tracks_url().format(id=str(artists_id)), params=params)



    def get_artists_related(self, artists_id):
        return self.__get_data(self.url.artists_related_url().format(id=str(artists_id)))


clientID = secrets.clientID
clientSecret = secrets.clientSecret

spotify = SpotifyAPI(clientID, clientSecret, response_format='json')
print(spotify.get_album_tracks("6kf46HbnYCZzP6rjvQHYzg"))
print(spotify.get_track("7l5j3FapCyr6HxUgoAynM2"))
print(spotify.get_track_audio_features("7l5j3FapCyr6HxUgoAynM2"))
print(spotify.get_artists_albums('3dv4Q4q3LWOnbLJnC6GgTY'))
print(spotify.get_artists_top_tracks('3dv4Q4q3LWOnbLJnC6GgTY'))
print(spotify.get_artists_related('3dv4Q4q3LWOnbLJnC6GgTY'))

"""
class Track:
    def __init__(self, title, spotify_id):
        print("test")

    def getTrack(spotify_token, trackID):
        query = f"https://api.spotify.com/v1/tracks/{trackID}"
        getheader = {
        "Content-Type": "json",
        "Authorization": "Bearer " + spotify_token
        }
        response = requests.get(query, headers=getheader)
        trackInfo = response.json()
        print(trackInfo['name'])
        return trackInfo





def getPlaylists(spotify_token, user_id):
    query = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    getheader = {
        "Content-Type": "json",
        "Authorization": "Bearer " + spotify_token
     }
    response = requests.get(query, headers=getheader)
    playlists = response.json()
    return playlists


def getPlaylistTracks(spotify_token, playlistID):
    query = f"https://api.spotify.com/v1/playlists/{playlistID}"
    getheader = {
        "Content-Type": "json",
        "Authorization": "Bearer " + spotify_token
    }
    response = requests.get(query, headers=getheader)
    playlistTracks = response.json()
    return playlistTracks





#API Requests
token = getAccessToken(secrets.clientID, secrets.clientSecret)

tracklist = getPlaylistTracks(token, "522eoPWDEPbY9neoxWzqM1?si=PCOenaAHTfy6IuCMMS1UBg")

for t in tracklist['tracks']['items']:
    print(t['track']['name'])

print("----")

playlists = getPlaylists(token, "kingboomie")

with open('playlists.json', 'w') as f:
    json.dump(playlists, f)

atID= "312WNtMs3F28cUukaPY9bo"
americanTeen = Track.getTrack(spotify_token=token, trackID=atID)
with open('americanTeen.json', 'w') as f:
    json.dump(americanTeen, f)
"""

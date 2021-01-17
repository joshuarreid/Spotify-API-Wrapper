import secrets
from src.__init__ import SpotifyAPI
import json
import time

clientID = secrets.clientID
clientSecret = secrets.clientSecret

spotify = SpotifyAPI(clientID, clientSecret, response_format='json')

artist_albums = spotify.get_artist_top_tracks('5K4W6rqBFWDnAN6FQUkS6x?si=1HO7DrYHTI2gRux5GqvmVg')




with open('artist_albums.json', 'w') as f:
    json.dump(artist_albums, f)
    

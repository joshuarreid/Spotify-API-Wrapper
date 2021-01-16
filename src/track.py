class Track:
    def __init__(self, name, album, artists, popularity, track_id, album_id, artists_id, duration_ms, explicit, release_date):
        self.name = name
        self.album = album
        self.artists = artists
        self.popularity = popularity
        self.track_id = track_id
        self.album_id = album_id
        self.artists_id = artists_id
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.release_date = release_date

    def __str__(self):
        return f"[name={self.name}, album={self.album}, artists={self.artists}, " \
               f"popularity={self.popularity}, track_id={self.track_id}, album_id={self.album_id}, " \
               f"artists_id={self.artists_id}, duration_ms={self.duration_ms}, explicit={self.explicit}, " \
               f"release_date={self.release_date}]"

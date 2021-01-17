class Album:
    def __init__(self, name, album_type, artists, album_id, copyrights, label, popularity, release_date, total_tracks, tracks):
        self.name = name
        self.album_type = album_type
        self.album_id = album_id
        self.artists = artists
        self.copyrights = copyrights
        self.label = label
        self.popularity = popularity
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.tracks = tracks

    def __str__(self):
        return f"[name={self.name}, album_id={self.album_id}, album_type={self.album_type}, " \
               f"artists={self.artists}, copyrights={self.copyrights}, label={self.label}, " \
               f"popularity={self.popularity}, release_date={self.release_date}, total_tracks={self.total_tracks}, " \
               f"tracks={self.tracks}]"







class Artist:
    def __init__(self, artist_id, name, popularity, genres):
        self.id = artist_id
        self.name = name
        self.popularity = popularity
        self.genres = genres

    def __str__(self):
        return F"[id={self.id}, name={self.name}, popularity={self.popularity}, genres={self.genres}]"




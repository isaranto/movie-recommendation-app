from datetime import datetime
class Movie:
    def __init__(self, json_dict):
        self.adult = json_dict["adult"]
        self.backdrop_path = json_dict["backdrop_path"]
        try:
            self.genre_ids = json_dict["genre_ids"]
        except KeyError:
            self.genre_ids = [g["id"] for g in json_dict["genres"]]
        self.id = json_dict["id"]
        self.original_language = json_dict["original_language"]
        self.original_title = json_dict["original_title"]
        self.overview = json_dict["overview"]
        self.popularity = json_dict["popularity"]
        self.poster_path = "https://image.tmdb.org/t/p/w300{0}".format(json_dict["poster_path"])
        self.release_date = json_dict["release_date"]
        try:
            self.release_year = datetime.strptime(json_dict["release_date"], '%Y-%m-%d').year
        except:
            self.release_year = ""
        #self.release_year = self.release_date.split("/")[0]
        self.title = json_dict["title"]
        self.video = json_dict["video"]
        self.vote_average = json_dict["vote_average"]
        self.vote_count = json_dict["vote_count"]


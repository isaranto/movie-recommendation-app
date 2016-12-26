import authenticate as auth
import requests
import json
import pprint
from Model import *
from picklecache import *
import os
import datetime
from Recommender import *

@cache('./cache/search')
def search(user_query, page_num=1):
    """
    Uses the MovieDB API to search for the given query.
    Results are being cached
    :param user_query: the search text
    :param page_num:
    :return:
    """
    if user_query == "start_page":
        total_pages = 0
        total_results = 0
        movies = []
    else:
        url = "https://api.themoviedb.org/3/search/movie"
        payload = {'query': user_query, 'api_key': auth.API_KEY, 'page': page_num}
        response = requests.request("GET", url, data=payload)
        json_data = json.loads(response.content)
        total_pages = json_data["total_pages"]
        total_results = json_data["total_results"]
        movies = []
        recommender = Recommender()
        for r in json_data["results"]:
            m = Movie(r)
            results = Movie(r).__dict__
            recom_ids = get_recommendations(recommender, m)
            recommendations = []
            for id in recom_ids:
                tuple = (get_movie_title(id),id)
                recommendations.append(tuple)
            results["recommendations"] = recommendations
            movies.append(results)
    return movies, total_pages, total_results


def get_recommendations(rec, m):
    return rec.recommend_movies(m.id)
    """return [("Lord of the Rings", "https://www.themoviedb.org/movie/"+str(120)),
            ("Fight Club", "https://www.themoviedb.org/movie/"+str(4))]"""

def get_movie_title(id):
    url = "https://api.themoviedb.org/3/movie/{0}".format(id)
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    movie_dict = json.loads(response.content)
    try:
        title = movie_dict['title']
    except KeyError:
        title = "Unknown Title"
    return title

@cache('./cache/genres')
def get_genres(_):
    """
    Uses the API to download genre info
    :return: returns a python dict of the form {genre_id : genre_name}
    """
    url = "https://api.themoviedb.org/3/genre/movie/list"
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    json_data = json.loads(response.content)
    genres = {}
    for gen in json_data["genres"]:
        genres[gen["id"]] = gen["name"]
    return genres


def get_poster(movie, size=300):
    """

    :param movie:
    :param size:
    :return:
    """
    url = "https://image.tmdb.org/t/p/w{0}{1}".format(size, movie.poster_path)
    """
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    with open("{}.jpg".format(movie.title), "w") as w:
        w.write(response.content)"""
    return url


def clear_cache():
    """
    compares every cache file timestamp to that of a week before and deletes
    cache files older than a week.
    """
    last_week = datetime.date.today() - datetime.timedelta(7)
    unix_time = float(last_week.strftime("%s"))
    for folder in os.listdir("./cache"):
        for file in os.listdir("./cache/"+folder):
            if os.path.getmtime("./cache/"+folder+"/"+file) < unix_time:
                os.remove("./cache/"+folder+"/"+file)

if __name__ == "__main__":
    movies, total_pages, total_results = search("Ariel")
    # pprint.pprint(results)
    #pprint.pprint(get_genres("_"))
    #movie = Movie(results[1])
    #get_poster(movie)
    #pprint.pprint(movies)
    #clear_cache()
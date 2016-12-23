import authenticate as auth
import requests
import json
import pprint
from Model import *


def search(user_query, page_num=1):
    """

    :param user_query:
    :param page_num:
    :return:
    """
    if user_query:
        url = "https://api.themoviedb.org/3/search/movie"
        payload = {'query': user_query, 'api_key': auth.API_KEY, 'page': page_num}
        response = requests.request("GET", url, data=payload)
        json_data = json.loads(response.content)
        total_pages = json_data["total_pages"]
        total_results = json_data["total_results"]
        movies = []
        for r in json_data["results"]:
            m = Movie(r)
            recommendations = get_recommendations(m)
            results = Movie(r).__dict__
            results["recommendations"] = recommendations
            movies.append(results)
    else:
        total_pages = 0
        total_results = 0
        movies = []
    return movies, total_pages, total_results


def get_recommendations(m):
    return ["Lord of the Rings", "Fight Club"]

def get_genres():
    """

    :return:
    """
    url = "https://api.themoviedb.org/3/genre/movie/list"
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    json_data = json.loads(response.content)
    genres = {}
    for gen in json_data["genres"]:
        genres[gen["id"]] = gen["name"]
    return genres


def get_poster(movie, size = 300):
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

if __name__ == "__main__":
    movies, total_pages, total_results = search("war")
    # pprint.pprint(results)
    # pprint.pprint(len(get_genres()))
    #movie = Movie(results[1])
    #get_poster(movie)
    pprint.pprint(movies)
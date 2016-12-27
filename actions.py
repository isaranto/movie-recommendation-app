import authenticate as auth
import requests
import json
import pprint
from Model import *
from picklecache import *
import os
import datetime
from Recommender import *
import pickle


@cache(auth.app_path+'cache/search')
def search(user_query, page_num=1):
    """
    Uses the MovieDB API to search for the given query.
    Add to the returned result the recommendations for each movie.
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
                tuple = (get_movie_title(id), "https://www.themoviedb.org/movie/"+str(id))
                recommendations.append(tuple)
            results["recommendations"] = recommendations
            movies.append(results)
    return movies, total_pages, total_results


def get_recommendations(rec, m):
    return rec.recommend_movies(m.id)

def get_movie_title(id):
    """
    Gets the movie title for the specified movie id
    from the json file
    url = "https://api.themoviedb.org/3/movie/{0}".format(id)
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    movie_dict = json.loads(response.content)"""
    if os.path.isfile(auth.app_path+'cache/movies.pickle'):
        with open(auth.app_path+'cache/movies.pickle', 'r') as handle:
            movies = pickle.load(handle)
    else:
        with open(auth.app_path+'movies.json', 'r') as fp:
            movies = json.loads(fp.read(), encoding="utf-8")
        with open(auth.app_path+'cache/movies.pickle', 'w') as handle:
            pickle.dump(movies, handle, protocol=pickle.HIGHEST_PROTOCOL)
    title = ""
    try:
        title = movies[str(id)]["title"]
    except KeyError:
        title = "Unknown Title"
    return title

@cache(auth.app_path+'cache/genres')
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


def get_poster(movie_id, size=300):
    """
    Get the url for the poster.
    A url string is being used instead of the API due to the request limit.
    :param movie: id
    :param size: the size of the poster
    :return:
    """
    url = "https://image.tmdb.org/t/p/w{0}{1}".format(size, movie.poster_path)
    """
    payload = {'api_key': auth.API_KEY}
    response = requests.request("GET", url, data=payload)
    with open("{}.jpg".format(movie.title), "w") as w:
        w.write(response.content)"""
    return url


def clear_cache(all=False):
    """
    compares every cache file timestamp to that of a week before and deletes
    cache files older than a week.
    Parameters
    ----------
    all: A boolean param to define wether we will delete everything or the cache
    entries of the last week.

    """
    if all:
        time_check = datetime.date.today() + datetime.timedelta(1)
    else:
        time_check = datetime.date.today() - datetime.timedelta(7)
    unix_time = float(time_check.strftime("%s"))
    for folder in os.listdir(auth.app_path+"cache"):
        for _file in os.listdir(auth.app_path+"cache/"+folder):
            try:
                print auth.app_path+"cache/"+folder+"/"+_file
                if os.path.getmtime(auth.app_path+"cache/"+folder+"/"+_file) < unix_time:
                    os.remove(auth.app_path+"cache/"+folder+"/"+_file)
                    print auth.app_path+"cache/"+folder+"/"+_file
            except OSError as e:
                # also delete the files under /cache/
                if ".tmp" not in e.filename:
                    if os.path.getmtime(e.filename) < unix_time:
                        os.remove(e.filename)

if __name__ == "__main__":
    movies, total_pages, total_results = search("ariel")
    # pprint.pprint(results)
    # pprint.pprint(get_genres("_"))
    # movie = Movie(results[1])
    # get_poster(movie)
    # pprint.pprint(movies)
    # clear_cache(all=True)

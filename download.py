import authenticate as auth
import requests
import json
import pprint
import ast
from Model import *
import time
import random

def get_movie(id):
    payload = {'api_key': auth.API_KEY}
    url = "https://api.themoviedb.org/3/movie/{0}".format(id)
    response = requests.request("GET", url, data=payload)
    json_data = json.loads(response.content)
    if response.status_code != 404:
        m = Movie(json_data)
    else:
        m = 404
    return m


def init_json():
    with open('movie_data.json', 'w') as fp:
        json.dump([], fp)



def write_json():
    with open('movie_data.json', mode='w') as feedsjson:
        data = []
        for i in range(1, 10000):
            if i % 40 == 0:
                time.sleep(11)
                print i
            m = get_movie(i)
            if m == 404:
                continue
            else:
                entry = m.__dict__
            data.append(entry)
        json.dump(data, feedsjson, indent=4)

def create_ratings(num_movies, num_users):
    with open('ratings.csv', 'w') as fp:
        for i in range(num_movies*20):
            user_id = random.randint(1, num_users)
            movie_id = random.randint(1, num_movies)
            rating = random.randint(1, 5)
            entry = str(user_id) + "," + str(movie_id) + "," + str(rating)
            fp.write(entry+"\n")

print "started!"
init_json()
write_json()



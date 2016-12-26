from __future__ import division
import pandas
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics import pairwise_distances
import csv
from picklecache import *

import os

path = '/home/lias/PycharmProjects/workable-assignment/'
class Recommender:
    def __init__(self, metric='cosine'):
        self.metric = metric
        self.predictions = self.make_predictions()

    def load_data(self):
        header = ['user_id', 'movie_id', 'rating']
        df = pd.read_csv('ratings.csv', sep=',', names=header)
        n_users = df.user_id.unique().shape[0]
        n_movies = df.movie_id.unique().shape[0]
        ratings = sparse.csr_matrix((n_users, n_movies))
        with open(path+'ratings.csv', 'r') as fp:
            reader = csv.reader(fp, delimiter=',')
            next(reader, None)  # skip header
            for row in reader:
                ratings[int(row[0])-1, int(row[1])-1] = int(row[2])

        return ratings


    def make_predictions(self):
        try:
            print "loading..."
            predictions = np.load(path+'cache/recommendations/predictions.npy')
            print os.path.dirname(os.path.realpath(__file__))
        except IOError:
            print "recalculating..."
            print os.path
            ratings = self.load_data()
            movie_similarity = pairwise_distances(ratings.T, metric='cosine')
            predictions = ratings.dot(movie_similarity) / np.array([np.abs(movie_similarity).sum(axis=1)])
            np.save(path+'cache/recommendations/predictions.npy', predictions)
        return predictions

    def recommend_movies(self, movie_id):
        try:
            print len(self.predictions[:, movie_id-1])
            movie_vector = self.predictions[:, movie_id-1]
            print movie_vector
            top_five_ids = movie_vector.argsort()[-5:][::-1]+1
            print top_five_ids
            print movie_vector[46]
        except IndexError:
            top_five_ids = [2, 3, 4, 5]
        return top_five_ids

if __name__ == '__main__':
    rec = Recommender('cosine')
    rec.recommend_movies(2)

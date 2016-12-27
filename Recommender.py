from __future__ import division
import pandas
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics import pairwise_distances
import authenticate as auth
import csv
from picklecache import *

import os



class Recommender:
    def __init__(self, metric='cosine', type='item'):
        self.type = type
        self.metric = metric
        self.predictions = self.make_predictions()

    def load_data(self):
        """
        Loads the ratings from the file ratings.csv and creates the User-Item matrix
        Returns
        -------

        """
        header = ['user_id', 'movie_id', 'rating']
        df = pd.read_csv(auth.app_path+'ratings.csv', sep=',', names=header)
        n_users = df.user_id.unique().shape[0]
        n_movies = df.movie_id.unique().shape[0]
        ratings = sparse.csr_matrix((n_users, n_movies))
        with open(auth.app_path+'ratings.csv', 'r') as fp:
            reader = csv.reader(fp, delimiter=',')
            next(reader, None)  # skip header
            for row in reader:
                ratings[int(row[0])-1, int(row[1])-1] = int(row[2])
        return ratings

    def make_predictions(self):
        """
        Calculates the predictions which will be used for recommending movies.
        Returns
        -------

        """
        try:
            # Trying to load the precalculated matrix from cache
            predictions = np.load(auth.app_path+'cache/recommendations/predictions.npy')
        except IOError:
            # if the cache doesn't exist we calculate again
            ratings = self.load_data()
            if self.type=='item':
                movie_similarity = pairwise_distances(ratings.T, metric='cosine')
                predictions = ratings.dot(movie_similarity) / np.array([np.abs(movie_similarity).sum(axis=1)])
                np.save(auth.app_path+'cache/recommendations/predictions.npy', predictions)
            elif self.type == 'user':
                user_similarity = pairwise_distances(ratings, metric='cosine')
                mean_user_rating = ratings.mean(axis=1)
                ratings_diff = ratings - np.repeat(mean_user_rating, ratings.shape[1], axis=1)
                pred = np.repeat(mean_user_rating,ratings.shape[1], axis=1)\
                       + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T
        return predictions

    def recommend_movies(self, movie_id):
        """
        Return the top five recommendations for the movie with the id supplied.

        """
        try:
            movie_vector = self.predictions[:, movie_id-1]
            top_five_ids = movie_vector.argsort()[-5:][::-1]+1
        except IndexError:
            top_five_ids = [2, 3, 4, 5]
        return top_five_ids

if __name__ == '__main__':
    rec = Recommender(metric='cosine')
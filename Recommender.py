from __future__ import division
import pandas
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics import pairwise_distances
class Recommender:
    def __init__(self, metric='cosine'):
        self.metric = metric
        self.ratings = self.load_data()

    def load_data(self):
        header = ['user_id', 'movie_id', 'rating']
        df = pd.read_csv('ratings.csv', sep=',', names=header)
        n_users = df.user_id.unique().shape[0]
        n_movies = df.item_id.unique().shape[0]
        ratings = sparse.csr_matrix(n_users, n_movies)
        return ratings

    def make_predictions(self):
        movie_similarity = pairwise_distances(self.ratings.T, metric='cosine')
        predictions = self.ratings.dot(movie_similarity) / np.array([np.abs(movie_similarity).sum(axis=1)])
        return predictions

if __name__=='__main__':
    red = Recommender('cosine')

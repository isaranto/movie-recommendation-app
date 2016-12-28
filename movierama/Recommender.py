from __future__ import division
import pandas
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics import pairwise_distances
import authenticate as auth
import csv
from picklecache import *
from copy import deepcopy
from scipy.optimize import fmin_cg
import os



class Recommender:
    def __init__(self, metric='cosine', type='item', method="CF"):
        self.type = type
        if method == "CF":
            self.metric = metric
            self.predictions = self.make_predictions()
        elif method == "SVD":
            self.predictions = self.matrix_completion()

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
            if self.type == 'item':
                movie_similarity = pairwise_distances(ratings.T, metric='cosine')
                predictions = ratings.dot(movie_similarity) / np.array([np.abs(movie_similarity).sum(axis=1)])
                np.save(auth.app_path+'cache/recommendations/predictions.npy', predictions)
            elif self.type == 'user':
                user_similarity = pairwise_distances(ratings, metric='cosine')
                mean_user_rating = ratings.mean(axis=1)
                ratings_diff = ratings - np.repeat(mean_user_rating, ratings.shape[1], axis=1)
                pred = np.repeat(mean_user_rating, ratings.shape[1], axis=1)\
                       + user_similarity.dot(ratings_diff) / np.array([np.abs(user_similarity).sum(axis=1)]).T
        return predictions


    def matrix_completion(self):
        """
        Uses the MatrixCompletion class to calculate the SVD
        Returns
        -------

        """
        try:
            # Trying to load the precalculated matrix from cache
            predictions = np.load(auth.app_path+'cache/recommendations/predictions.npy')
        except IOError:
            # if the cache doesn't exist we calculate again
            if os.path.isfile(auth.app_path+'cache/recommendations/initial_ratings.npy'):
                ratings = np.load(auth.app_path+'cache/recommendations/initial_ratings.npy')[()]
            else:
                ratings = self.load_data()
                np.save(auth.app_path+'cache/recommendations/initial_ratings.npy', ratings)
                print ratings.shape
            m = MatrixCompletion(ratings).X_aproks
            np.save(auth.app_path+'cache/recommendations/predictions.npy', predictions)
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


class MatrixCompletion:
    def __init__(self, ratings):
        self.X = ratings
        self.R = self.create_R()
        print "created R and X"
        self.X_aproks = self.optimize()

    def create_R(self):
        R = deepcopy(self.X.todense())
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                if R[i, j] == 0:
                    R[i, j] = 0
                else:
                    R[i, j] = 1
        return R

    def cost_function(self, params, X, R, k):
        error = 0

        U = np.reshape(params[:X.shape[0]*k], (X.shape[0], k), order='F')
        V = np.reshape(params[X.shape[0]*k:], (k, X.shape[1]), order='F')

        print U.shape
        print V.shape

        m = np.dot(U, V)

        print m.shape

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                error += (X[i,j] - m[i,j]) ** 2 if X[i,j] > 0 else 0

        return error

    def gradient(self, params, X, R, k):
        numUsers = X.shape[0]
        numMovies = X.shape[1]

        # Unfold the U and V matrices from params
        U = np.reshape(params[:numUsers*k], (numUsers, k), order='F')
        V = np.reshape(params[numUsers*k:], (k, numMovies), order='F')

        U_grad = np.zeros(U.shape)
        V_grad = np.zeros(V.shape)

        # calculating gradient of U
        for i in range(numUsers):
            non_empty_cols = R[i, :]==1
            V_tmp = V[:, (R[i, :]==1)[0, :]]
            X_tmp = X[i, R[i, :]==1]
            U_grad[i, :] = np.dot((np.dot(U[i, :],V_tmp) - X_tmp),V_tmp.T)

        # calculating gradient of V
        for j in range(numMovies):
            U_tmp = U[R[:, j] == 1, :]
            X_tmp = X[R[:, j] == 1, j]
            V_grad[:, j] = np.dot(np.transpose(np.dot(U_tmp,V[:, j]) - X_tmp),U_tmp)

        return np.concatenate((U_grad.flatten('F'), V_grad.flatten('F')))

    def optimize(self):
        k=3
        U = np.random.randn(self.X.shape[0], k)
        V = np.random.randn(k, self.X.shape[1])
        initial_parameters = np.concatenate((U.flatten('F'),V.flatten('F')))
        params = fmin_cg(self.cost_function, initial_parameters, fprime=self.gradient, args=(self.X.todense(), self.R,
                                                                                             k),
                         maxiter=100)
        U = np.reshape(params[:self.X.shape[0]*k], (self.X.shape[0], k), order='F')
        V = np.reshape(params[self.X.shape[0]*k:], (k, self.X.shape[1]), order='F')
        X_approx = np.dot(U, V)
        return X_approx

if __name__ == '__main__':
    rec = Recommender(metric='cosine')
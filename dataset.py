#dependencies
import pandas as pd
import numpy as np
from pathlib import Path

#main class
class Graph:

    def __init__(self, movie_path, rating_path):
        self.movies = pd.read_csv(movie_path, sep=',')
        self.ratings = pd.read_csv(rating_path, sep=',')

        #clip dataset
        self.ratings = self.ratings[self.ratings['userId'] < 300]
        self.ratings = self.ratings[self.ratings['movieId'] < 1000]
        self.movies = self.movies[self.movies['movieId'] < 1000]

    def bipartiteGraphUserMovie(self):
        
        users = list(self.ratings.userId.unique())
        movies = list(self.movies.movieId.unique())

        num_users = len(users)
        num_movies = len(movies)

        self.bipartiteGraph = np.zeros((num_users, num_movies))
        
        users = list(self.ratings.userId.unique())
        movies = list(self.movies.movieId.unique())
        
        for name, group in self.ratings.groupby(["userId", "movieId"]):
            user_id, movie_id = name
            user_index = users.index(user_id)
            movie_index = movies.index(movie_id)

            self.bipartiteGraph[user_index, movie_index] = group[["rating"]].values[0,0] 

    def constructGraph(self):
        matfile = Path('./numpy-file/ratingMatrix.npy')

        if matfile.exists():
            self.loadMatrixToNumpyFile()
            print('loaded file\n')

        else:
            self.bipartiteGraphUserMovie()

    def loadMatrixToNumpyFile(self):
        self.bipartiteGraph = np.load('./numpy-file/ratingMatrix.npy') 
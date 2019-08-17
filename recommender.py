import numpy as np 
import argparse
import operator

class Recommender:

    #------initialize all members------# 
    def __init__(self, graph, userId):
        
        self.userId = userId
        
        self.graph = graph

        self.genres = list(self.graph.movies.genres)
        self.movieId = list(self.graph.movies.movieId)
        self.movieTitles = list(self.graph.movies.title)

        self.movieDict = dict(zip(self.movieId, self.movieTitles))
        
        self.genreDict = {}
        self.genreRateAccumulator = {}

    #------if user not present in graph add to graph-----#
    def addUserToGraph(self):

        if(self.userId > self.graph.ratings["userId"].unique()[-1]):
            self.graph.bipartiteGraph = np.append(self.graph.bipartiteGraph, np.zeros((1, 807)), axis = 0)
     

    #------genres dictionary------#
    def makeGenreDict(self):
        
        num_movies = self.graph.movies["movieId"].unique().shape[0]

        for i in range(num_movies):
            if(self.graph.bipartiteGraph[self.userId][i]>0):
                g_movie = list(self.genres[i].split("|"))

                for j in range(len(g_movie)):

                    if(g_movie[j] in self.genreDict.keys() and g_movie[j] in self.genreRateAccumulator.keys()):

                        self.genreDict[g_movie[j]] = self.genreDict[g_movie[j]] + 1
                        self.genreRateAccumulator[g_movie[j]] = self.genreRateAccumulator[g_movie[j]] + self.graph.bipartiteGraph[self.userId][i]

                    else:
                        self.genreDict[g_movie[j]] = 1
                        self.genreRateAccumulator[g_movie[j]] = self.graph.bipartiteGraph[self.userId][i]

        for key in self.genreDict.keys():
            self.genreRateAccumulator[key] = self.genreRateAccumulator[key] / self.genreDict[key] 

        self.genreRateAccumulator = sorted(self.genreRateAccumulator.items(), key = operator.itemgetter(1))

    #-----recommend function-----#
    def recommend(self):
        
        self.recommendDict = {}
        self.recommendDict.clear()

        self.makeGenreDict()

        self.top5Genres = []
        self.top5Genres.append(self.genreRateAccumulator[-1][0])
        self.top5Genres.append(self.genreRateAccumulator[-2][0])
        self.top5Genres.append(self.genreRateAccumulator[-3][0])
        self.top5Genres.append(self.genreRateAccumulator[-4][0])
        self.top5Genres.append(self.genreRateAccumulator[-5][0])

        counter = [0, 0, 0, 0, 0]

        for k in range(len(self.movieTitles)):
            
            if(self.top5Genres[0] in self.genres[k] and counter[0] <= 2 and self.graph.bipartiteGraph[self.userId][k] == 0):
                # print(self.movieTitles[k])
                self.recommendDict[self.movieId[k]] = self.movieTitles[k]
                counter[0] = counter[0] + 1

            if(self.top5Genres[1] in self.genres[k] and counter[1] <= 2 and self.graph.bipartiteGraph[self.userId][k] == 0):
                # print(self.movieTitles[k])
                self.recommendDict[self.movieId[k]] = self.movieTitles[k]
                counter[1] = counter[1] + 1

            if(self.top5Genres[2] in self.genres[k] and counter[2] <= 2 and self.graph.bipartiteGraph[self.userId][k] == 0):
                # print(self.movieTitles[k])
                self.recommendDict[self.movieId[k]] = self.movieTitles[k]
                counter[2] = counter[2] + 1

            if(self.top5Genres[3] in self.genres[k] and counter[3] <= 2 and self.graph.bipartiteGraph[self.userId][k] == 0):
                # print(self.movieTitles[k])
                self.recommendDict[self.movieId[k]] = self.movieTitles[k]
                counter[3] = counter[3] + 1

            if(self.top5Genres[4] in self.genres[k] and counter[4] <= 2 and self.graph.bipartiteGraph[self.userId][k] == 0):
                # print(self.movieTitles[k])
                self.recommendDict[self.movieId[k]] = self.movieTitles[k]
                counter[4] = counter[4] + 1
        
        for key, value in self.recommendDict.items():
            print(str(key) + " " + value + '\n')   

    def saveMatrixToNumpyFile(self):
        np.save('./numpy-file/ratingMatrix.npy', self.graph.bipartiteGraph)


import numpy as np 
from recommender import Recommender
from dataset import Graph
from search import searchTrie
import argparse
import operator

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--movie_path", required = True, help = "Path to movies.csv directory")
ap.add_argument("-r", "--ratings_path", required = True, help = "Path to ratings.csv directory")

args = vars(ap.parse_args())

class User:
    
    f = open("user.txt", 'r')
    userIdgen = int(f.read())
    f.close()
    
    def __init__(self, name, userId = None, new = True):
        self.name = name

        if(new):
            self.userId = User.userIdgen + 1
            User.userIdgen = User.userIdgen + 1
            
            f = open('user.txt', 'w')
            f.seek(0)
            f.write(str(User.userIdgen))
            f.truncate()
            f.close()

        else:
            self.userId = userId

    def watchAndrateMovie(self, movieId, recommender):
        print(recommender.movieDict[movieId] + "-- rate on a scale of 1 - 5: ")
        rating = int(input())
        recommender.graph.bipartiteGraph[self.userId][movieId] = rating

    def searchMovie(self, searchTrieObj, keyword, titles, movieId):
        found = searchTrieObj.search(keyword)
        if(found):
            dict_ID={}
            for k in titles:
                if(k[0:len(keyword)].lower()== keyword):
                    ind = titles.index(k)
                    dict_ID[movieId[ind]]=k
            print("Choose your movies which you want to watch")
            for key,values in dict_ID.items():
                if(key<807):
                    print(str(key) +"  "+str(values)+ '\n')
        else:
            print("No such movie with this Keyword")
            exit(0)
        


def main():

    graph = Graph(args["movie_path"], args["ratings_path"])
    graph.constructGraph()

    print("")
    print("Are you a new user [y/n]: ")

    a = str(input())

    if(a == 'y' or a == 'Y'):  
        print("Enter your name: ")
        name = str(input())
        user = User(name)
        recommender = Recommender(graph, user.userId)
        recommender.addUserToGraph()
        trie = searchTrie(recommender.movieTitles)
        print("Search for keyword: ")
        keyword = str(input())
        user.searchMovie(trie, keyword, recommender.movieTitles, recommender.movieId)
        print("Enter movieId from above to watch and rate: ")
        movieId = list(map(int,input().split(" ")))

        for x in movieId:
            user.watchAndrateMovie(x, recommender)
        print("Here are some recommendations for you\n")
        recommender.recommend()


        recommender.saveMatrixToNumpyFile()
        

    
    else:
        print("Enter your userId(1 to 297): ")
        userId = int(input())
        print("Enter your name: ")
        name = str(input())
        user = User(name, userId, new = False)
        recommender = Recommender(graph, user.userId)
        print("Here are some recommendations for you\n")
        recommender.recommend()


    

    

if __name__ == '__main__':
    main()

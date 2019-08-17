from pathlib import Path
from six.moves import cPickle as pickle

class searchTrie:
    def __init__(self, titles):
        self.rootDict = {}
        triefile = Path('./data/trie.pkl')

        if triefile.exists():
            with open('./data/trie.pkl', 'rb') as f:
                self.rootDict = pickle.load(f)

        else:
            self.buildSearchTrie(titles)

    def insert(self, word):
        currentDict = self.rootDict

        for letter in word:
            keys = currentDict.keys()
            if(letter not in keys):
                newDict = {}
                currentDict[letter] = newDict
            currentDict = currentDict[letter]
        
        with open('./data/trie.pkl', 'wb') as f:
            pickle.dump(self.rootDict, f)

    def search(self, wordToBeSearched):
        if len(wordToBeSearched) != 0:
            if len(self.rootDict) != 0:
                currentDict = self.rootDict
                flag = 0

                for letter in wordToBeSearched:
                    keys = currentDict.keys()
                    if letter in keys:
                        currentDict = currentDict[letter]
                        flag = 1

                    else:
                        flag = 0
                        break

            else:
                print("Search Trie is empty!\n\n")
        else:
            print("Enter valid search string\n\n")
        return flag

    def buildSearchTrie(self, titles):
        for k in titles:
            self.insert(k[0 : len(k) - 7].lower())
        
        with open('./data/trie.pkl', 'wb') as f:
            pickle.dump(self.rootDict, f)

        


            

import shelve
import os
import indexer
from tokenizer import Tokenizer


class SearchEngine(object):
    """Class that contains mathods for searching in a database

    """
    def __init__(self, database_name):
        """Create an instance of SearchEngine class

        @param database_name -- filename of the databased searched

        """
        self.database = shelve.open(database_name)

    def search(self, query):
        """Search database and return filenames
        and positions for the searched word

        @param query -- word, positions of which are returned 

        """
        if not isinstance(query, str):
            raise TypeError('Inappropriate argument type.')
        if query not in self.database:
            return {}        
        return self.database[query]

    def search_multiple(self, query):
        """Search database and return filenames
        and positions for one or more words

        @param query -- one or more words, positions of which are returned

        """
        if not isinstance(query, str):
            raise TypeError('Inappropriate argument type.')
        if query == '':
            return {}
        token = Tokenizer()
        words = list(token.words_and_numbers_tokenize(query))
        results = []
        keys = []
        for word in words:
            if word.string not in self.database:
                return {}
            dic = self.database[word.string]
            results.append(set(dic))
            for key in dic:
                keys.append(key)
        keys = set(keys)
        # remove files in which not all the searched words are present
        for files in results:
            keys &= files
        positions = {}
        for file in keys:
            for word in words:
                positions.setdefault(file, []).extend(self.database[word.string][file])
        return positions
            

    def __del__(self):
        """Close database when searching is done

        """
        self.database.close()


def main():    
    index = indexer.Indexer('db')    
    t = open('tst.txt', 'w')
    t.write(' this is my test\nthis is my test\nthis is my test')
    t.close()
    d = open('tgt.txt', 'w')
    d.write(' is\nmy test  ')
    d.close()
    index.indexing_with_lines('tst.txt')
    index.indexing_with_lines('tgt.txt')
    del index
    engine = SearchEngine('db')
    result = engine.search_multiple('my test is ')
    del engine
    print(result)
    if 'tgt.txt' in os.listdir(os.getcwd()):
        os.remove('tgt.txt')
    if 'tst.txt' in os.listdir(os.getcwd()):
        os.remove('tst.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'db' or filename.startswith('db.'):
            os.remove(filename) 
    
        
if __name__=='__main__':
    main()

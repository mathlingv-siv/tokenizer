import shelve
import os
import indexer


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
            raise TypeError('Inappropriate argumant type.')
        if query == '' or query not in self.database:
            return {}
        return self.database[query]

    def __del__(self):
        """Close database when searching is done

        """
        self.database.close()


def main():    
    index = indexer.Indexer('database')    
    t = open('tst.txt', 'w')
    t.write('test')
    t.close()
    index.indexing_with_lines('tst.txt')
    del index
    engine = SearchEngine('database')
    result = engine.search('test')
    del engine
    print(result)    
    if 'tst.txt' in os.listdir(os.getcwd()):
        os.remove('tst.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename) 
    
        
if __name__=='__main__':
    main()

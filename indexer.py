"""This module contains methods for indexing text files

"""
from tokenizer import Tokenizer
import shelve
import os


class Position(object):
    """Class for token's position in the text file

    """
    def __init__(self, start, end):
        """Create an instance of class Position

        @start -- position of the first character in the token
        @end -- position of the last character in the token
        
        """
        self.start = start
        self.end = end

    def __eq__(self, obj):
        """Override how to compare instances of class Position

        """
        return self.start == obj.start and self.end == obj.end

    def __repr__(self):
        """Override what to return when print an instance of class Position

        """
        return '(' + str(self.start) + ',' + ' ' + str(self.end) + ')'

    
class Indexer(object):
    """Class that contains methods for indexing text files

    """
    def __init__(self, database_name):
        """Create an instance of class Indexer

        @param database_name -- filename of the database created
        
        """
        self.database = shelve.open(database_name, writeback = True)

    def indexing(self, filename):
        """Index a text file and fill in database

        @param filename -- name of the text file that is to be indexed

        """
        if (not isinstance(filename, str) or filename.endswith('.txt') != True):
            raise TypeError('Inappropriate argument type.')
        tokenizator = Tokenizer()
        text = open(filename)
        # divide text into alphabetic and digital tokens
        # add tokens, filenames and positions to the database
        for word in tokenizator.words_and_numbers_tokenize(text.read()):
            i = word.position + len(word.string)
            self.database.setdefault(word.string, {}).setdefault(filename, []).append(Position(word.position, i))
        text.close()
        self.database.sync()

    def __del__(self):
        """Close database after indexing is done

        """
        self.database.close()


def main():
    f = open('text.txt', 'w')
    f.write('this is a test test')
    f.close()
    index = Indexer('database')
    index.indexing('text.txt')
    t = open('ts.txt', 'w')
    t.write('this this')
    t.close()
    index.indexing('ts.txt')
    del index
    os.remove('text.txt')
    os.remove('ts.txt')
    print(dict(shelve.open('database')))
    for filename in os.listdir(os.getcwd()):            
        if filename == 'database' or filename.startswith('database.'):
            os.remove(filename)   


if __name__=='__main__':
    main()

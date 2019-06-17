"""This module contains methods for searching in a database

"""
import shelve
import os
import indexer
from indexer import Position_with_lines
from tokenizer import Tokenizer


class Context_Window(object):
    def __init__(self, position, start, end, string):
        self.start = start
        self.end = end
        self.string = string
        self.position = position        

    def __eq__(self, obj):        
        return (self.position == obj.position and self.start == obj.start and
                   self.end == obj.end and self.string == obj.string)

    def __repr__(self):
        return str(self.string[self.start:self.end])

        
class SearchEngine(object):
    """Class that contains mathods for searching in a database
    """
    def __init__(self, database_name):
        """Create an instance of SearchEngine class
        @param database_name: filename of the databased searched
        """
        self.database = shelve.open(database_name)

    def search(self, query):
        """Search database and return filenames
        and positions for the searched word
        @param query: word, positions of which are returned 
        """
        if not isinstance(query, str):
            raise TypeError('Inappropriate argument type.')
        if query not in self.database:
            return {}        
        return self.database[query]

    def search_multiple(self, query):
        """Search database and return filenames
        and positions for one or more words
        @param query: one or more words, positions of which are returned
        """
        if not isinstance(query, str):
            raise TypeError('Inappropriate argument type.')
        if query == '':
            return {}
        tokenization = Tokenizer()
        words = list(tokenization.words_and_numbers_tokenize(query))
        results = []
        for word in words:
            if word.string not in self.database:
                return {}
            results.append(self.database[word.string])        
        files = set(results[0])
        for result in results[1:]:
            files &= set(result)
        positions = {}
        for file in files:
            for result in results:
                positions.setdefault(file, []).extend(result[file])
            positions[file].sort()
        return positions
    
    def search_one_context(self, filename, position, window):
        """find a context window for one word
        @param filename: name of the file containing the word
        @param position: Position_with_lines object
        @param window: size of the context window (how many words
        should be found on the right and  on the left of the word)
        @return dictionary: object of Context_Window class, containing positions
        and context window of the searched word
        """
        if not isinstance(filename, str):
            raise TypeError('Inappropriate argument type.')
        start = 0
        end = 0
        found = False
        with open(filename) as filetext:
            for ln, string in enumerate(filetext):
                if ln == position.line:
                    text = string
                    found = True
        if not found:
            raise ValueError('Line not found')        
        if position.end > len(text) or position.end <= position.start:
            raise ValueError('Position not found')
        if not window:
            return Context_Window([position], position.start, position.end, text)
        tokenization = Tokenizer()
        wordlist = list(tokenization.words_and_numbers_tokenize(text))
        word_found = False
        for token in wordlist:
            if token.string == text[position.start:position.end]:
                word_found = True
        if word_found == False:
            raise TypeError('Word not found')
        right_context = list(tokenization.words_and_numbers_tokenize(text.strip('\n')[position.start:]))
        left_context = list(tokenization.words_and_numbers_tokenize(text.strip('\n')[:position.end]))
        left_context.reverse()
        for i, token in enumerate(left_context):
            if i == window:
                start = token.position
                break        
        for i, token in enumerate(right_context):
            if len(right_context) == 1:
                end = position.end
            elif i == window:
                end = position.start + token.position + len(token.string)
                break
            else:
                if window >= len(right_context):
                    end = position.start + right_context[-1].position + len(right_context[-1].string)
        context = Context_Window([position], start, end, text)
        return context

    def unite_windows(self, dictionary):
        """intersect context windows
        @param: dictionary {filename: context windows}
        @return: dictionary {filename: united context windows}

        """
        for key, value in dictionary.items():
            i = 0
            while i < len(value)-1:
                if value[i].position[0].line == value[i+1].position[0].line:
                    if value[i+1].start < value[i].end and value[i].start < value[i+1].end:
                        value[i].end = value[i+1].end
                        value[i].position.extend(value[i+1].position)
                        value.remove(value[i+1])
                    else:
                        i+=1
                else:
                    i+=1
        return dictionary
    
    def search_multiple_contexts(self, search_result, window):
        """find context windows for one or more words
        @param search_result: dictionary {filename: positions}
        with positions of the searched words in the files that contain them        
        @param window: size of the context window (how many words
        should be found on the right and  on the left of the word)
        @return: dictionary {filename: intersected context windows}
        """
        dic = {}
        pos = []
        #create a dictionary {filename: context windows}
        for key in search_result:
            for position in search_result[key]:
                cw = self.search_one_context(key, position, window)
                pos.append(cw)
            dic.setdefault(key, []).extend(pos)
            pos = []
        dictionary = self.unite_windows(dic)
        return dictionary       

    def __del__(self):
        """Close database when searching is done
        """
        self.database.close()


def main():    
    index = indexer.Indexer('db')    
    d = open('tgt.txt', 'w')
    d.write('this is a test required for helping students create a test\n')
    d.write(' professor required to write a test first')
    d.close()
    index.indexing_with_lines('tgt.txt')
    t = open('ttt.txt', 'w')
    t.write('test is required. On the other hand...')
    t.close()
    index.indexing_with_lines('ttt.txt')
    del index
    engine = SearchEngine('db')
    search = engine.search_multiple('test required')
    result = engine.search_one_context('tgt.txt', Position_with_lines(11, 19, 1), 1)
    result_multiple = engine.search_multiple_contexts(search, 3)
    print(result_multiple)
    del engine
    if 'tgt.txt' in os.listdir(os.getcwd()):
        os.remove('tgt.txt')
    if 'ttt.txt' in os.listdir(os.getcwd()):
        os.remove('ttt.txt')
    for filename in os.listdir(os.getcwd()):            
        if filename == 'db' or filename.startswith('db.'):
            os.remove(filename) 
    
        
if __name__=='__main__':
    main()

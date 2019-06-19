import unittest
import tokenizer
import os
import shelve
import indexer
from indexer import Position
from indexer import Position_with_lines
from search_engine import SearchEngine
from search_engine import Context_Window


class TestContextWindows(unittest.TestCase):
    """Class that contains methods for testing
    if the code for finding context windows is working correcly in different cases
    """
    def setUp(self):
        index = indexer.Indexer('database')        
        f = open('test.txt', 'w')
        f.write('this is a test required for helping students create a test\n')
        f.write(' professor required to write a test first')
        f.close()
        t = open('tst.txt', 'w')
        t.write('test is required. On the other hand...')
        t.close()        
        index.indexing_with_lines('test.txt')
        index.indexing_with_lines('tst.txt')
        del index
        self.s = SearchEngine('database')

    def test_hcw(self):
        """test if the program is working correctly
        when searching for contexts windows
        with the searched words highlighted
        
        """
        result = self.s.search_highlighted_context('test required', 2)
        output = {'test.txt': ['is a <b>test</b> <b>required</b> for helping','create a <b>test</b>',
                               ' professor <b>required</b> to write a <b>test</b> first'],
                  'tst.txt': ['<b>test</b> is <b>required</b>. On the']}
        self.assertEqual(result, output)

    def test_scw(self):
        """test if the program is working correctly
        when searching for context windows extended to
        the sentence boundaries

        """
        result = self.s.search_extended_context('test required', 2)
        output = {'test.txt': [Context_Window([Position_with_lines(10, 14, 0), Position_with_lines(15, 23, 0),
                                               Position_with_lines(54, 58, 0)], 0, 58, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(11, 19, 1), Position_with_lines(31, 35, 1)], 0, 41, ' professor required to write a test first')],
                  'tst.txt': [Context_Window([Position_with_lines(0, 4, 0), Position_with_lines(8, 16, 0)], 0, 38, 'test is required. On the other hand...')]}
        self.assertEqual(result, output)

    def test_scw_single(self):
        """test if the program is working correctly
        when searching for context windows extended to
        the sentence boundaries for a single word

        """
        k = open('newtest.txt', 'w')
        k.write('What is your name? My name is test.')
        k.close()
        ind = indexer.Indexer('newdb')
        ind.indexing_with_lines('newtest.txt')
        del ind
        self.k = SearchEngine('newdb')
        result = self.k.search_extended_context('test', 1)
        output = {'newtest.txt': [Context_Window([Position_with_lines(30, 34, 0)], 19, 35, 'What is your name? My name is test.')]}
        self.assertEqual(result, output)
        del self.k
        for filename in os.listdir(os.getcwd()):            
            if filename == 'newdb' or filename.startswith('newdb.'):
                os.remove(filename)        
        os.remove('newtest.txt')

    def test_mcw_singleword_one(self):
        """test if the program is working correctly
        when searching for contexts of a word with window = 1
        
        """
        query = self.s.search_multiple('test')
        result = self.s.search_multiple_contexts(query, 1)
        output = {'test.txt': [Context_Window([Position_with_lines(10, 14, 0)], 8, 23, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(54, 58, 0)], 52, 58, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(31, 35, 1)], 29, 41, ' professor required to write a test first')],
                  'tst.txt': [Context_Window([Position_with_lines(0, 4, 0)], 0, 7, 'test is required. On the other hand...')]}
        self.assertEqual(result, output)

    def test_mcw_twowords_one(self):
        """test if the program is working correctly
        when searching for contexts of two words with window = 1
        
        """
        query = self.s.search_multiple('test required')
        result = self.s.search_multiple_contexts(query, 1)
        output = {'test.txt': [Context_Window([Position_with_lines(10, 14, 0), Position_with_lines(15, 23, 0)], 8, 27, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(54, 58, 0)], 52, 58, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(11, 19, 1)], 1, 22, ' professor required to write a test first'),
                               Context_Window([Position_with_lines(31, 35, 1)], 29, 41, ' professor required to write a test first')],
                  'tst.txt': [Context_Window([Position_with_lines(0, 4, 0), Position_with_lines(8, 16, 0)], 0, 20, 'test is required. On the other hand...')]}
        self.assertEqual(result, output)

    def test_mcw_two(self):
        """test if the program is working correctly
        when searching for contexts of two words with window = 2
        
        """
        query = self.s.search_multiple('test required')
        result = self.s.search_multiple_contexts(query, 2)
        output = {'test.txt': [Context_Window([Position_with_lines(10, 14, 0), Position_with_lines(15, 23, 0)], 5, 35, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(54, 58, 0)], 45, 58, 'this is a test required for helping students create a test'),
                               Context_Window([Position_with_lines(11, 19, 1), Position_with_lines(31, 35, 1)], 0, 41, ' professor required to write a test first')],
                  'tst.txt': [Context_Window([Position_with_lines(0, 4, 0), Position_with_lines(8, 16, 0)], 0, 24, 'test is required. On the other hand...')]}
        self.assertEqual(result, output)

    def test_cw_one_token(self):
        """test if the program is working correctly
        when searching for context of a word with window = 1
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(10, 14, 0), 1)
        self.window = Context_Window([Position_with_lines(10, 14, 0)], 8, 23, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_one_null(self):
        """test if the program is working correctly
        when searching for context of a word with window = 0
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(10, 14, 0), 0)
        self.window = Context_Window([Position_with_lines(10, 14, 0)], 10, 14, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_one_out_of_range(self):
        """test if the program is working correctly
        when searching for context of a word with window > text length
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(10, 14, 0), 10)
        self.window = Context_Window([Position_with_lines(10, 14, 0)], 0, 58, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_two_one_token(self):
        """test if the program is working correctly
        when searching for context of a word with window = 2
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(10, 14, 0), 2)
        self.window = Context_Window([Position_with_lines(10, 14, 0)], 5, 27, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)        

    def test_cw_three_one_token(self):
        """test if the program is working correctly
        when searching for context of a word with window = 3
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(10, 14, 0), 3)
        self.window = Context_Window([Position_with_lines(10, 14, 0)], 0, 35, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_no_left_one_token(self):
        """test if the program is working correctly
        when searching for context of a word with no left context
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(0, 4, 0), 3)
        self.window = Context_Window([Position_with_lines(0, 4, 0)], 0, 14, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_no_right_one_token(self):
        """test if the program is working correctly
        when searching for context of a word with no right context
        
        """
        result = self.s.search_one_context('test.txt', Position_with_lines(54, 58, 0), 3)
        self.window = Context_Window([Position_with_lines(54, 58, 0)], 36, 58, 'this is a test required for helping students create a test')
        self.assertEqual(result.start, self.window.start)
        self.assertEqual(result.end, self.window.end)
        self.assertEqual(result.position, self.window.position)
        self.assertEqual(result.string, self.window.string)

    def test_cw_position_end_error(self):
        """test if the program is working correctly
        when searching for context of a word with error in its end position
        
        """
        with self.assertRaises(ValueError):
            self.s.search_one_context('test.txt', Position_with_lines(10, 140, 0), 1)

    def test_cw_start_equal_end(self):
        """test if the program is working correctly
        when searching for context of a word with start position = end position
        
        """
        with self.assertRaises(ValueError):
            self.s.search_one_context('test.txt', Position_with_lines(14, 14, 0), 1)

    def test_cw_end_start_error(self):
        """test if the program is working correctly
        when searching for context of a word with start position > end position
        
        """
        with self.assertRaises(ValueError):
            self.s.search_one_context('test.txt', Position_with_lines(14, 10, 0), 1)

    def test_cw_line_error(self):
        """test if the program is working correctly
        when searching for context of a word with error in its line number
        
        """
        with self.assertRaises(ValueError):
            self.s.search_one_context('test.txt', Position_with_lines(10, 14, 90), 1)

    def test_cw_line_neg_error(self):
        """test if the program is working correctly
        when searching for context of a word with a negative line number
        
        """
        with self.assertRaises(ValueError):
            self.s.search_one_context('test.txt', Position_with_lines(10, 14, -1), 1)

    def test_cw_no_word_error(self):
        """test if the program is working correctly
        when searching for context of a position that does not correspond to any word
        
        """
        with self.assertRaises(TypeError):
            self.s.search_one_context('test.txt', Position_with_lines(3, 8, 0), 1)

    def test_cw_filename_error(self):
        """test if the program is working correctly
        when searching for context of a word with error in its filename
        
        """
        with self.assertRaises(TypeError):
            self.s.search_one_context(567, Position_with_lines(10, 14, 0), 1)

    
            
    def tearDown(self):
        del self.s
        for filename in os.listdir(os.getcwd()):            
            if filename == 'database' or filename.startswith('database.'):
                os.remove(filename)        
        if 'test.txt' in os.listdir(os.getcwd()):
            os.remove('test.txt')
        if 'tst.txt' in os.listdir(os.getcwd()):
            os.remove('tst.txt')

        
class TestSearchEngine(unittest.TestCase):
    """Class that contains methods for testing
    if search engine is working correcly in different cases
    """
    def setUp(self):
        index = indexer.Indexer('database')        
        f = open('test.txt', 'w')
        f.write('this is\ntest')
        f.close()
        t = open('tst.txt', 'w')
        t.write('test')
        t.close()        
        index.indexing_with_lines('test.txt')
        index.indexing_with_lines('tst.txt')
        del index
        self.s = SearchEngine('database')

    def test_searching_is_string(self):
        """test if the program is working correctly
        when searching for a not alphabetic object
        
        """
        with self.assertRaises(TypeError):
            self.s.search(345)
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            self.s.search(array)

    def test_searching_empty_string(self):
        """test if the program is working correctly
        when searching for an empty string
        
        """
        result = self.s.search('')
        self.assertEqual(result, {})

    def test_searching_none(self):
        """test if the program is working correctly
        when searching for a word that is not in the database
        
        """        
        result = self.s.search('a')
        self.assertEqual(result, {})

    def test_searching(self):
        """test if the program is working correctly
        when searching for one word
        
        """
        result = self.s.search('test')
        self.assertEqual(result, {'test.txt': [Position_with_lines(0, 4, 1)],
                                  'tst.txt': [Position_with_lines(0, 4, 0)]})

    def test_searching_more_than_one_token(self):
        """test if the program is working correctly
        when searching for more than one word
        
        """
        result = self.s.search('this is')
        self.assertEqual(result, {})

    def test_search_multiple_is_string(self):
        """test if engine for multiple word search
        is working correctly when searching
        for a not alphabetic object
        
        """
        with self.assertRaises(TypeError):
            self.s.search_multiple(345)
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            self.s.search_multiple(array)

    def test_search_multiple_empty_string(self):
        """test if engine for multiple word search
        is working correctly when searching
        for an empty string
        
        """
        result = self.s.search_multiple('')
        self.assertEqual(result, {})

    def test_search_multiple_none(self):
        """test if engine for multiple word search
        is working correctly when searching
        for a word that is not in the database
        
        """        
        result = self.s.search_multiple('a')
        self.assertEqual(result, {})

    def test_search_multiple_one_token(self):
        """test if engine for multiple word search
        is working correctly when searching for one word
        
        """
        result = self.s.search_multiple('test')
        self.assertEqual(result, {'test.txt': [Position_with_lines(0, 4, 1)],
                                  'tst.txt': [Position_with_lines(0, 4, 0)]})

    def test_search_multiple(self):
        """test if engine for multiple word search
        is working correctly when searching
        for more than one word
        
        """
        result = self.s.search_multiple('this is')
        self.assertEqual(result, {'test.txt': [Position_with_lines(0, 4, 0),
                                               Position_with_lines(5, 7, 0)]})

    def test_search_multiple_not_all(self):
        """test if engine for multiple word search
        is working correctly when not all the
        searched words are present in the database
        """
        result = self.s.search_multiple('this is a')
        self.assertEqual(result, {})

    def tearDown(self):
        del self.s
        for filename in os.listdir(os.getcwd()):            
            if filename == 'database' or filename.startswith('database.'):
                os.remove(filename)        
        if 'test.txt' in os.listdir(os.getcwd()):
            os.remove('test.txt')
        if 'tst.txt' in os.listdir(os.getcwd()):
            os.remove('tst.txt')


class TestIndexer(unittest.TestCase):
    """Class that contains methods for testing
    if indexer is working correctly in different cases
    
    """
    def setUp(self):
        """create an object of Indexer class 
        """
        self.i = indexer.Indexer('database')
        
    def test_indexing_is_file(self):
        """test if the program is working correctly
        when indexing non-file objects
        
        """
        with self.assertRaises(TypeError):
            self.i.indexing(345)
        with self.assertRaises(FileNotFoundError):
            self.i.indexing('this is a test')
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            self.i.indexing(array)

    def test_indexing(self):
        """test if the program is working correctly
        when indexing a single file
        
        """       
        f = open('test.txt', 'w')
        f.write('this is a test test')
        f.close()        
        self.i.indexing('test.txt')        
        db_dict = dict(shelve.open('database'))
        dictionary = {
            'this': {'test.txt': [Position(0, 4)]},
            'is': {'test.txt': [Position(5, 7)]},
            'a': {'test.txt': [Position(8, 9)]},
            'test': {'test.txt': [Position(10, 14), Position(15, 19)]}
        }
        self.assertEqual(db_dict, dictionary) 

    def test_indexing_multiple_files(self):
        """test if the program is working correctly
        when indexing multiple files
        
        """        
        p = open('test.txt', 'w')
        p.write('is this a test?')
        p.close()        
        self.i.indexing('test.txt')        
        s = open('ts.txt', 'w')
        s.write('yes, it is a test')
        s.close()  
        self.i.indexing('ts.txt')
        db_dict = dict(shelve.open('database'))
        dictionary = {
            'is': {'test.txt': [Position(0, 2)], 'ts.txt': [Position(8, 10)]},
            'this': {'test.txt': [Position(3, 7)]},
            'a': {'test.txt': [Position(8, 9)], 'ts.txt': [Position(11, 12)]},
            'test': {'test.txt': [Position(10, 14)], 'ts.txt': [Position(13, 17)]},
            'yes': {'ts.txt': [Position(0, 3)]},
            'it': {'ts.txt': [Position(5, 7)]}
        }
        self.assertEqual(db_dict, dictionary)

    def test_indexing_with_lines(self):
        """test if the program is working correctly
        when indexing a single file
        
        """       
        f = open('test.txt', 'w')
        f.write('this is\n a test\n test')
        f.close()        
        self.i.indexing_with_lines('test.txt')        
        db_dict = dict(shelve.open('database'))
        dictionary = {
            'this': {'test.txt': [Position_with_lines(0, 4, 0)]},
            'is': {'test.txt': [Position_with_lines(5, 7, 0)]},
            'a': {'test.txt': [Position_with_lines(1, 2, 1)]},
            'test': {'test.txt': [Position_with_lines(3, 7, 1), Position_with_lines(1, 5, 2)]}
        }
        self.assertEqual(db_dict, dictionary)

    def tearDown(self):
        """delete Indexer object, text and database files
        
        """
        del self.i
        for filename in os.listdir(os.getcwd()):            
            if filename == 'database' or filename.startswith('database.'):
                os.remove(filename)        
        if 'test.txt' in os.listdir(os.getcwd()):
            os.remove('test.txt')
        if 'ts.txt' in os.listdir(os.getcwd()):
            os.remove('ts.txt')
                

class TestTokenizer(unittest.TestCase):
    """Class that contains methods for testing
    if tokenizer is working correctly in different cases
    
    """
    def setUp(self):
        """create an object of Tokenizer class
        """
        self.t = tokenizer.Tokenizer()
   
    def test_is_string(self):
        """test if the programm is working correctly
        when tokenizing a non-string object or an empty string    
        """
        with self.assertRaises(TypeError):
            self.t.tokenize(789)
        with self.assertRaises(TypeError):
            self.t.tokenize('')
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            self.t.tokenize(array)        
   
    def test_first_character_is_alpha(self):
        """test if the programm is working correctly
        when the first character is alphabetic
    
        """
        text = self.t.tokenize('this is a test')
        self.assertEqual(len(text), 4)
        self.assertEqual(text[0].string, 'this')
        self.assertEqual(text[0].position, 0)        
    
    def test_first_character_is_not_alpha(self):
        """test if the programm is working correctly
        when the first character is not alphabetic
    
        """
        text = self.t.tokenize(' 23 4 this is a test')
        self.assertEqual(len(text), 4)
        self.assertEqual(text[0].string, 'this')
        self.assertEqual(text[0].position, 6)        
    
    def test_last_character_is_alpha(self):
        """test if the programm is working correctly
        when the last character is alphabetic
    
        """
        text = self.t.tokenize('this is a test')
        self.assertEqual(len(text), 4)
        self.assertEqual(text[3].string, 'test')
        self.assertEqual(text[3].position, 10)        
    
    def test_last_character_is_not_alpha(self):
        """test if the programm is working correctly
        when the last character is not alphabetic
    
        """
        text = self.t.tokenize('this is a test 890')
        self.assertEqual(len(text), 4)
        self.assertEqual(text[3].string, 'test')
        self.assertEqual(text[3].position, 10)

    def test_tokenize_words_only(self):
        """test if the programm is working correctly
        when several non-alpha characters follow each other
    
        """
        text = self.t.tokenize('...test. And...')
        self.assertEqual(len(text), 2)
        self.assertEqual(text[0].string, 'test')
        self.assertEqual(text[0].position, 3)
        self.assertEqual(text[1].string, 'And')
        self.assertEqual(text[1].position, 9)

    def test_gen_is_string(self):
        """test if the programm is working correctly
        when tokenizing a non-string object or an empty string    
        """
        with self.assertRaises(TypeError):
            list(self.t.gen_tokenize(789))
        with self.assertRaises(TypeError):
            list(self.t.gen_tokenize(''))
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            list(self.t.gen_tokenize(array))        
 
    def test_gen_first_character_is_alpha(self):
        """test if the programm is working correctly
        when the first character is alphabetic
    
        """
        text = list(self.t.gen_tokenize('this is a test'))
        self.assertEqual(len(text), 4)
        self.assertEqual(text[0].string, 'this')
        self.assertEqual(text[0].position, 0)        
    
    def test_gen_first_character_is_not_alpha(self):
        """test if the programm is working correctly
        when the first character is not alphabetic
    
        """
        text = list(self.t.gen_tokenize(' 23 4 this is a test'))
        self.assertEqual(len(text), 4)
        self.assertEqual(text[0].string, 'this')
        self.assertEqual(text[0].position, 6)        
    
    def test_gen_last_character_is_alpha(self):
        """test if the programm is working correctly
        when the last character is alphabetic
    
        """
        text = list(self.t.gen_tokenize('this is a test'))
        self.assertEqual(len(text), 4)
        self.assertEqual(text[3].string, 'test')
        self.assertEqual(text[3].position, 10)        
    
    def test_gen_last_character_is_not_alpha(self):
        """test if the programm is working correctly
        when the last character is not alphabetic
    
        """
        text = list(self.t.gen_tokenize('this is a test 890'))
        self.assertEqual(len(text), 4)
        self.assertEqual(text[3].string, 'test')
        self.assertEqual(text[3].position, 10)

    def test_gen_tokenize_words_only(self):
        """test if the programm is working correctly
        when several non-alpha characters follow each other
    
        """
        text = list(self.t.gen_tokenize('...test. And...'))
        self.assertEqual(len(text), 2)
        self.assertEqual(text[0].string, 'test')
        self.assertEqual(text[0].position, 3)
        self.assertEqual(text[1].string, 'And')
        self.assertEqual(text[1].position, 9)

    def test_type_string(self):
        """test if the program assigns the right type
        to alphabetic characters
        """
        text = list(self.t.type_aware_tokenize('and'))
        self.assertEqual(text[0].type, 'a')

    def test_type_digit(self):
        """test if the program assigns the right type
        to numeric characters
        """        
        text = list(self.t.type_aware_tokenize('123'))
        self.assertEqual(text[0].type, 'd')

    def test_type_space(self):
        """test if the program assigns the right type
        to spaces
        """        
        text = list(self.t.type_aware_tokenize('k p'))
        self.assertEqual(text[1].type, 's')

    def test_type_punc(self):
        """test if the program assigns the right type
        to punctuation marks
        """        
        text = list(self.t.type_aware_tokenize('k, p'))
        self.assertEqual(text[1].type, 'p')

    def test_type_other(self):
        """test if the program assigns the right type
        to other kinds of characters
        """
        text = list(self.t.type_aware_tokenize('+'))
        self.assertEqual(text[0].type, 'o')


    def test_type_aware(self):
        """test if the type aware tokenizer is working correctly
    
        """
        text = list(self.t.type_aware_tokenize('...test. And...'))
        self.assertEqual(len(text), 6)
        self.assertEqual(text[0].string, '...')
        self.assertEqual(text[0].position, 0)
        self.assertEqual(text[1].string, 'test')
        self.assertEqual(text[1].position, 3)
        self.assertEqual(text[2].string, '.')
        self.assertEqual(text[2].position, 7)
        self.assertEqual(text[5].string, '...')
        self.assertEqual(text[5].position, 12)
        
    def test_type_aware_non_string(self):
        """test if the programm is working correctly
        when tokenizing a non-string object or an empty string    
        """
        with self.assertRaises(TypeError):
            list(self.t.type_aware_tokenize(789))
        with self.assertRaises(TypeError):
            list(self.t.type_aware_tokenize(''))
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            list(self.t.type_aware_tokenize(array))

    def test_words_and_numbers(self):
        text = list(self.t.words_and_numbers_tokenize('hello. 2 45, bye?'))
        self.assertEqual(len(text), 4)
        self.assertEqual(text[0].string, 'hello')
        self.assertEqual(text[0].position, 0)
        self.assertEqual(text[1].string, '2')
        self.assertEqual(text[1].position, 7)
            


if __name__=='__main__':
    unittest.main()

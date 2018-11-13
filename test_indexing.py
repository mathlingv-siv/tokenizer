import unittest
import tokenizer
import os
import shelve


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.i = tokenizer.Indexer('database')
        
    def test_indexing_is_file(self):
        with self.assertRaises(TypeError):
            self.i.indexing(345)
        with self.assertRaises(TypeError):
            self.i.indexing('this is a test')
        array = [25, 'array', '79 - 0']
        with self.assertRaises(TypeError):
            self.i.indexing(array)

    def test_indexing_create_database(self):
        f = open('test.txt', 'w')
        f.write('this is a test')
        f.close()        
        self.i.indexing('test.txt')
        db = shelve.open('database')
        db_dict = dict(db)
        dictionary = {
            'this':{'test.txt': '[0, 4]'},
            'is':{'test.txt': '[5, 7]'},
            'a':{'test.txt':'[8, 9]'},
            'test':{'test.txt':'[10, 14]'}
        }
        self.assertEqual(db_dict, dictionary)      
        os.remove('test.txt')
        db.close()
        for filename in os.listdir(os.getcwd()):
            if filename == 'database' and filename.startswith('database.'):
                os.remove(filename)

    def test_indexing_multiple_files(self):
        p = open('tf.txt', 'w')
        p.write('is this a test?')
        p.close()        
        self.i.indexing('tf.txt')        
        s = open('ts.txt', 'w')
        s.write('yes, it is a test')
        s.close()        
        self.i.indexing('ts.txt')
        db = shelve.open('database')
        db_dict = dict(db)
        dictionary = {
            'is':{'tf.txt':'[0, 2]', 'ts.txt':'[8, 10]'},
            'this':{'tf.txt':'[3, 7]'},
            'a':{'tf.txt':'[8, 9]', 'ts.txt':'[11, 12]'},
            'test':{'tf.txt':'[10, 14]', 'ts.txt':'[13, 17]'},
            'yes':{'ts.txt':'[0, 3]'},
            'it':{'ts.txt':'[5, 7]'}
        }
        self.assertEqual(db_dict, dictionary)
        os.remove('ts.txt')
        os.remove('tf.txt')
        db.close()
        for filename in os.listdir(os.getcwd()):
            if filename == 'database' and filename.startswith('database.'):
                os.remove(filename)
        


if __name__=='__main__':
    unittest.main()

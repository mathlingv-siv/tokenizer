import unittest
import tokenizer


class TestTokenizer(unittest.TestCase):
    """Class that contains methods for testing
    if the programm is working correctly in different cases
    
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


if __name__=='__main__':
    unittest.main()

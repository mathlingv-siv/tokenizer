"""This module contains a method for tokenizing a string of characters
    
"""
class Token(object):
    """Class for tokens the text is divided into
        
    """    
    def __init__(self, p, s):
        """Initialize token

        @param p -- position of the first character in the token
        @param s -- string representation of the token
        
        """
        self.position = p
        self.string = s
        
    def __repr__(self):
        """Override what to return when print tokens

        """
        return self.string + ' ' + str(self.position)


class Tokenizer(object):
    """Class that contains method for tokenizing a string of characters
        
    """
    def tokenize(self, string):
        """Divides a string into tokens consisting only of alphabetic symbols  

        @param string -- text to be divided into tokens
        
        @return words -- list of tokens

        """
        if (not isinstance(string, str) or len(string) == 0):
            raise TypeError('Inappropriate argument type.')
        words = []       
        for index, character in enumerate(string):
            # find the beginning of a token
            # it's either the first character in the string
            # or the character that is alpha while the previous one is not
            if character.isalpha() and (index == 0 or not string[index-1].isalpha()):                             
                a = index
            # check if we haven't reached the end of the string
            # we check the following symbol, so we need to make sure that there's one
            if (index+1)<=(len(string)-1):
                # find the end of the token and add it to the list
                if character.isalpha() and not string[index+1].isalpha():
                    token = string[a:index+1]
                    t = Token(a,token)
                    words.append(t)
        # the last character in the string wasn't checked in the cycle
        # add the last token to the list if it's alphabethic
        if character.isalpha():
                token = string[a:index+1]
                t = Token(a,token)
                words.append(t)
        return words

    
    def gen_tokenize(self, string):
        """Token generator  

        @param string -- text to be divided into tokens
        
        @return words -- list of tokens

        """
        if (not isinstance(string, str) or len(string) == 0):
            raise TypeError('Inappropriate argument type.')
        for index, character in enumerate(string):
            # find the beginning of a token
            # it's either the first character in the string
            # or the character that is alpha while the previous one is not
            if character.isalpha() and (index == 0 or not string[index-1].isalpha()):                             
                a = index
            # check if we haven't reached the end of the string
            # we check the following symbol, so we need to make sure that there's one
            if (index+1)<=(len(string)-1):
                # find the end of the token 
                if character.isalpha() and not string[index+1].isalpha():
                    token = string[a:index+1]
                    t = Token(a,token)
                    yield (t)
        # the last character in the string wasn't checked in the cycle        
        if character.isalpha():
                token = string[a:index+1]
                t = Token(a,token)
                yield (t)
        

def main():
    text = Tokenizer()
    print(text.tokenize('t his, is a ??? test?'))
    for i in text.gen_tokenize('t his, is a ??? test?'):
        print(i)
    
if __name__=='__main__':
    main()



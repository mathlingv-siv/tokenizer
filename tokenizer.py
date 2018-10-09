"""This module contains a method for tokenizing a string of characters
    
"""
import unicodedata

def what_type(c):
    category = ''
    if c.isalpha():
        category = 'a'
    else:
        if c.isdigit():
            category = 'd'            
        else:
            if c.isspace():
                category = 's'
            else:
                if unicodedata.category(c)[0] == 'P':
                    category = 'p'
                else:
                    category = 'o'
    return category
                  
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
    
class Token_type_aware(object):
    """Class for different kinds of tokens the text is divided into

    """
    def __init__(self, pos, st, ty):
        """Initialize token

        @param pos -- position of the first character in the token
        @param st -- string representation of the token
        @param ty -- type of the token
        
        """
        self.position = pos
        self.string = st
        self.type = ty

    def __repr__(self):
        """Override what to return when print tokens

        """
        return '"' + self.string + '"' + '[' + str(self.position) + ']' + '{' + self.type + '}'


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
    def type_aware_tokenize(self, string):
        """type aware token generator

        """
        if (not isinstance(string, str) or len(string) == 0):
            raise TypeError('Inappropriate argument type.')
        for index, character in enumerate(string):
            category = what_type(character)
            # find the beginning of a token
            # it's either the first character in the string
            # or the character the type of which is different from the type of the previous one
            if index == 0 or not category == what_type(string[index-1]):
                a = index
            # check if we haven't reached the end of the string
            # we check the following symbol, so we need to make sure that there's one
            if (index+1)<=(len(string)-1):
                # find the end of the token
                if category != what_type(string[index+1]):
                    token = string[a:index+1]
                    t = Token_type_aware(a, token, category)
                    a = index+1
                    yield (t)
        # the last character in the string wasn't checked in the cycle  
        token = string[a:index+1]
        t = Token_type_aware(a, token, category)
        yield (t)              
                

def main():
    text = Tokenizer()
    print(text.tokenize('this, is a ??? test?'))
    for i in text.gen_tokenize('this, is a ??? test?'):
        print(i)
    for i in text.type_aware_tokenize('this, is a ??? test?'):
        print(i)
    
if __name__=='__main__':
    main()



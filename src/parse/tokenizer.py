import re
from exceptions import LexerException

# Lexer

# Types
EOF = "EOF"
NL = "NEWLINE"

L_OP = "LOGICAL_OPERATOR"
L_PAREN = "LEFT_PARENTHESIS"
R_PAREN = "RIGHT_PARENTHESIS"
L_BRACKET = "LEFT_BRACKET"
R_BRACKET = "RIGHT_BRACKET"

B_BLCK = "BEGIN_BLOCK"
OP = "OPERATOR"
D_QUOTE = "DOUBLE_QUOTE"
ASSIGN = "ASSIGNMENT"

NUM = "NUMBER"
ID = "IDENTIFIER"
KEY = "KEYWORD"

class Token:
    def __init__(self,line,literal,type):
        self.line = line
        self.literal = literal
        self.type = type

    def __repr__(self):
        return f'{self.line} | {self.type} : {repr(self.literal)}'

class Tokenizer:
    def __init__(self,source):
        self.i = 0
        if len(source) > 0:
            self.curtok = source[self.i]

        self.source = source
        self.line = 1
        self.tokens = []

        self.keywords = [
            "check","while",
            "func","return",
            "continue","break",
            "true","false",
            "print", "end"
        ]

    def lex(self):
        while self.i < len(self.source):
            c = self.source[self.i]
            cp = self.peek()
            if c == '~':
                while self.source[self.i] != '\n': 
                    self.advance() 
                    print(c)
            elif c == '\n':
                self.tokens.append(Token(self.line,c,NL))
                self.line += 1
            elif c == '-':
                self.double_lexeme(c,cp,'>',OP,ASSIGN)
            elif c == "\"":
                self.tokens.append(Token(self.line,c,D_QUOTE))
            elif c in ('>','<','!'): 
                self.double_lexeme(c,cp,'=',L_OP)
            elif c == '=': 
                self.tokens.append(Token(self.line,c,L_OP))
            elif c == ':':
                self.tokens.append(Token(self.line,c,B_BLCK))
            elif self.m("[][]",c):
                self.tokens.append(Token(self.line,c,L_BRACKET if c == '[' else R_BRACKET))
            elif str.isdecimal(c): 
                self.tokens.append(Token(self.line,self.get_digit(),NUM))
            elif str.isalpha(c) or c in ("_"):
                self.tokens.append(self.get_char_token())
            elif self.m("[+/*^%]",c): 
                self.tokens.append(Token(self.line,c,OP))
            elif self.m("[()]",c): 
                self.tokens.append(Token(self.line,c,L_PAREN if c == '(' else R_PAREN))

            self.advance()
        self.append_EOF()
        return self.tokens

    #TODO: Change these parameter names to better reflect their purpose.
    def double_lexeme(self, c, cp, expected_seek, type1, type2=L_OP):
        if cp != expected_seek:
            self.tokens.append(Token(self.line,c,type1))
        else:
            self.tokens.append(Token(self.line,c+cp,type2))
            self.advance()

    def m(self, pat, char):
        return re.match(pat,char) != None

    def peek(self):
        index = self.i + 1
        return self.source[index] if index < len(self.source) else None
        
    def get_char_token(self):
        result = self.seek_m("[a-zA-Z_]")
        return Token(self.line, result, ID) if result not in self.keywords else Token(self.line,result,KEY)

    def get_digit(self):
        #TODO Improve regex for scanning floats.
        return float(self.seek_m("[0-9.]"))

    def seek_m(self, pat):
        found = ""
        for index in range(self.i,len(self.source)):
            if self.source[index] != None and re.match(pat, str(self.source[index])) != None:
                found+=self.source[index]
                self.advance()
            else: break
        self.i-=1 #TODO: Fix later
        return found

    def advance(self):
        self.i+=1
    
    def append_EOF(self):
        self.tokens.append(Token(self.line,"",EOF))

    def print_tokens(self):
        for Token in self.tokens: print(Token)
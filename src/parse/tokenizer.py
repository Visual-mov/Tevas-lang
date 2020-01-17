import re
from exceptions import LexerException

# Lexer

# Types
EOF = "EOF"

L_OP = "LOGICAL_OPERATOR"
L_PAREN = "LEFT_PARENTHESIS"
R_PAREN = "RIGHT_PARENTHESIS"
L_BRACKET = "LEFT_BRACKET"
R_BRACKET = "RIGHT_BRACKET"

B_BLCK = "BEGIN_BLOCK"
OP = "OPERATOR"
ASSIGN = "ASSIGNMENT"

NUM = "NUMBER"
STR = "STRING"
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
    def __init__(self,source,line=None):
        self.i = 0
        if len(source) > 0:
            self.curtok = source[self.i]
        self.source = source
        self.line = 1 if line == None else line
        self.tokens = []

        self.keywords = [
            "check", "celse",
            "else", "while",
            "true","false",
            "print", "println",
            "end", "continue",
            "break"
        ]

    def lex(self):
        while self.i < len(self.source):
            c = self.source[self.i]
            cp = self.peek()
            if c == '~':
                self.scan("\n")
            elif c == '\n':
                self.line += 1
            elif c == '-':
                self.double_lexeme(c,cp,'>',OP,ASSIGN)
            elif c == "\"":
                self.tokens.append(Token(self.line,self.scan(c),STR))
                self.advance()
            elif c in ('>','<','!'): 
                self.double_lexeme(c,cp,'=',L_OP)
            elif c == '=': 
                self.tokens.append(Token(self.line,c,L_OP))
            elif c == self.peek():
                if c in ('&','|'): self.tokens.append(Token(self.line,c + self.peek(),L_OP))
            elif c == ':':
                self.tokens.append(Token(self.line,c,B_BLCK))
            elif self.m("[][]",c):
                self.tokens.append(Token(self.line,c,L_BRACKET if c == '[' else R_BRACKET))
            elif str.isdecimal(c): 
                self.tokens.append(Token(self.line,self.get_digit(),NUM))
            elif str.isalpha(c) or c in ('_'):
                self.tokens.append(self.get_char_token())
            elif self.m("[+/*^%]",c): 
                self.tokens.append(Token(self.line,c,OP))
            elif self.m("[()]",c): 
                self.tokens.append(Token(self.line,c,L_PAREN if c == '(' else R_PAREN))
            
            self.advance()
        self.append_EOF()
        return self.tokens

    def m(self, pat, char):
        return re.match(pat,char) != None

    def peek(self):
        index = self.i + 1
        return self.source[index] if index < len(self.source) else None
        
    def get_char_token(self):
        result = self.scan_match("[a-zA-Z_0-9]")
        return Token(self.line, result, ID) if result not in self.keywords else Token(self.line,result,KEY)
    
    def get_digit(self):
        val = self.scan_match("[0-9.]")
        try: return float(val)
        except ValueError:
            raise LexerException(self.line,"Error lexing Float")

    def double_lexeme(self, c, cp, expected_seek, type1, type2=L_OP):
        if cp != expected_seek:
            self.tokens.append(Token(self.line,c,type1))
        else:
            self.tokens.append(Token(self.line,c+cp,type2))
            self.advance()
        
    def scan(self, expected_c):
        found = ""
        for index in range(self.i,len(self.source)):
            c = self.source[index]
            found += c if c != expected_c else ""
            if self.peek() == expected_c: break
            elif c == EOF or index == len(self.source) - 1:
                raise LexerException(self.line,f"Expected '{expected_c}' character")
            else: self.advance()
        return found

    def scan_match(self, pat):
        found = ""
        for index in range(self.i,len(self.source)):
            if re.match(pat, str(self.source[index])) != None:
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
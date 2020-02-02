import re, sys
from parse.parser import Parser
from parse.tokenizer import Tokenizer
import eval.evaluator as eval

# The Tex Programming Language
# www.github.com/Visual-mov/Tex-lang
#
# Copywrite(c) Ryan Danver (Visual-mov) 2019

DEBUG = False

def repl(argv):
    run = True
    g_table = eval.SymbolTable()

    if len(argv)-1 > 1 and argv[1] == "--file":
        try:
            try:
                source = open(argv[2], 'r').read()
            except FileNotFoundError:
                repl_error(f"Can not find file: \"{argv[2]}\"")
            tokenizer = Tokenizer(source)
            tokens = tokenizer.lex()
            if DEBUG: tokenizer.print_tokens()

            ast = Parser(tokens).parse()
            if DEBUG: print(str(ast) + '\n')

            evaluator = eval.Evaluator(ast, g_table, False)
            evaluator.eval()
        except KeyboardInterrupt:
            repl_error()
    else:
        print("Tex Language REPL\nCreated by Ryan Danver 2019")
        line = 1
        while run:
            try: 
                eval.Evaluator(Parser(Tokenizer(input(">> ").replace('\n',''), line).lex()).parse(), g_table, True).eval()
            except KeyboardInterrupt:
                repl_error()
            line += 1

def repl_error(message=""):
    print(message)
    exit()

if __name__ == "__main__":
    repl(sys.argv)
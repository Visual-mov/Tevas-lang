import re, sys
from parse.parser import Parser
from parse.tokenizer import Tokenizer
import eval.evaluator as eval

# The Tevas Programming Language
# www.github.com/Visual-mov/Tevas-lang

DEBUG = True

def repl(argv):
    run = True
    table = eval.SymbolTable()

    if len(argv) == 2:
        try:
            source = open(argv[1], 'r').read()
            tokenizer = Tokenizer(source)
            tokens = tokenizer.lex()
            if DEBUG: tokenizer.print_tokens()

            ast = Parser(tokens).parse()
            if DEBUG: print(str(ast) + '\n')

            evaluator = eval.Evaluator(ast, table, False)
            evaluator.evaluate()
        except FileNotFoundError:
            repl_error(f"Can not find file: \"{argv[1]}\"")
    else:
        print("Tevas Language Shell")
        line = 1
        while run:
            try: 
                eval.Evaluator(Parser(Tokenizer(input(">> ").replace('\n',''), line).lex()).parse(), table, True).evaluate()
            except KeyboardInterrupt:
                repl_error()
            line += 1

def repl_error(message=""):
    print(message)
    exit()

if __name__ == "__main__":
    repl(sys.argv)
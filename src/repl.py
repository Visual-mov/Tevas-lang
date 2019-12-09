import re
import sys
from parse.parser import Parser
from parse.tokenizer import Tokenizer
import eval.evaluator as eval

# The Tex Programming Language REPL v1.0
# www.github.com/Visual-mov/Tex-lang
#
# Copywrite(c) Ryan Danver 2019

def repl(argv):
    run = True
    line = 1
    gTable = eval.SymbolTable()

    if len(argv)-1 > 1 and argv[1] == "--file":
        source = open(argv[2],'r').read()

        tokenizer = Tokenizer(source)
        tokens = tokenizer.lex()
        tokenizer.print_tokens()
        ast = Parser(tokens).parse()
        print(str(ast) + '\n')
        evaluator = eval.Evaluator(ast,gTable)
        evaluator.eval()
        #eval.Evaluator(Parser(Tokenizer(source,line).lex()).parse(),gTable).eval()
    else:
        # REPL
        print("Tex Language v1.0")
        while run:
            
            # Create the list of tokens.
            tokenizer = Tokenizer(input(">> ") + "\n")
            tokens = tokenizer.lex()
            tokenizer.print_tokens()

            # Create the AST
            ast = Parser(tokens).parse()
            print(ast)

            # Execute the AST.
            evaluator = eval.Evaluator(ast,gTable)
            evaluator.eval()

            line+=1

if __name__ == "__main__":
    repl(sys.argv)
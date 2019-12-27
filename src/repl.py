import re, sys
from parse.parser import Parser
from parse.tokenizer import Tokenizer
import eval.evaluator as eval

# The Tex Programming Language v1.0
# www.github.com/Visual-mov/Tex-lang
#
# Copywrite(c) Ryan Danver 2019

def repl(argv):
    run = True
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
        print("Tex Language REPL v1.0")
        while run:
            
            # Create the list of tokens.
            tokens = Tokenizer(input(">> ") + "\n").lex()

            # Create the AST
            ast = Parser(tokens).parse()

            # Execute the AST.
            eval.Evaluator(ast,gTable).eval()

if __name__ == "__main__":
    repl(sys.argv)
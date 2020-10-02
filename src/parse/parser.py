from exceptions import ParserException
from parse.nodes import *
import parse.tokenizer as tokenizer

# Parser class
# Creates Abstract Syntax Tree (AST) from tokens array.  
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        if len(self.tokens) > 0:
            self.curtok = tokens[self.index]
        else: self.curtok = None

    def parse(self):
        if self.curtok == None: return
        else: return self.program()
    
    # Helper functions
    def advance(self):
        self.index+=1
        if self.index < len(self.tokens):
            self.curtok = self.tokens[self.index]
        return self.curtok

    def consume(self, type, literal):
        if self.curtok.type == type and self.curtok.literal == literal:
            self.advance()
            return True
        else: raise ParserException(self.curtok.line, literal, "ex")

    def bin_op(self, func, ops):
        l = func()
        while self.curtok.literal in ops and not self.curtok.literal == "":
            op = self.curtok.literal
            self.advance()
            r = func()
            l = BinaryOpNode(l, op, r, self.curtok.line)
        return l

    def cond_stmt(self, key):
        self.consume(tokenizer.KEY, key)
        self.consume(tokenizer.L_BRACKET, '[')
        expr = self.cmpnd_expr()
        self.consume(tokenizer.R_BRACKET, ']')
        self.consume(tokenizer.B_BLCK, ':')
        return expr

    # Productions (See language grammar)
    def factor(self):
        tok = self.curtok
        if tok.type == tokenizer.NUM:
            self.advance()
            return NumNode(tok.literal, tok.line)
        elif tok.type == tokenizer.ID:
            self.advance()
            return AccessNode(tok.literal, tok.line)
        elif tok.type == tokenizer.EOF:
            raise ParserException(self.curtok, tokenizer.EOF, "unex")
        elif tok.literal == "true" or tok.literal == "false":
            self.advance()
            return BooleanNode(1 if tok.literal == "true" else 0, tok.line)
        elif tok.type == tokenizer.STR:
            self.advance()
            return StringNode(tok.literal, tok.line)
        elif tok.literal in ("+", "-"):
            self.advance()
            return UnaryOpNode(tok.literal, self.factor(), tok.line)
        elif tok.literal == '(':
            self.advance()
            expr = self.a_expr()
            if self.curtok.literal == ')':
                self.advance()
                return expr
            else:
                raise ParserException(tok.line, "Expected ')'")
        else: raise ParserException(tok.line, tok.literal, "unex")

    def term(self):
        return self.bin_op(self.factor, ("*", "/", "%"))

    def a_expr(self):
        return self.bin_op(self.term, ("+", "-"))

    def l_expr(self):
        if self.curtok.literal == '!':
            self.advance()
            return UnaryOpNode("!", self.l_expr(), self.curtok.line)
        else:
            return self.bin_op(self.a_expr, ("=", "!=", "<=", ">=", "<", ">"))

    def cmpnd_expr(self):
        return self.bin_op(self.l_expr, ("&&", "||"))

    def assignment(self):
        expr = self.cmpnd_expr()
        if self.curtok.type == tokenizer.ASSIGN:
            self.advance()
            id = self.factor()
            if isinstance(id, AccessNode):
                return AssignmentNode(expr, id.id, self.curtok.line)
            else:
                raise ParserException(self.curtok.line, "Identifier", "ex")
        else: return expr

    def print_stmt(self, key):
        self.advance()
        expr = self.cmpnd_expr()
        return PrintNode(expr, self.curtok.line, True if key == "println" else False)

    def else_stmt(self):
        self.consume(tokenizer.KEY, "else")
        self.consume(tokenizer.B_BLCK, ':')
        return ElseNode(self.block_stmt(), self.curtok.line)

    def ifelse_stmt(self):
        expr = self.cond_stmt("celse")
        block = self.block_stmt()
        return CelseNode(expr, block, self.curtok.line)

    def if_stmt(self):
        expr = self.cond_stmt("check")
        block = self.block_stmt()
        celse_stmts = []
        else_stmt = None
        while self.curtok.literal == "celse":
            celse_stmts.append(self.ifelse_stmt())
        if self.curtok.literal == "else":
            else_stmt = self.else_stmt()
        return CheckNode(expr, block, celse_stmts, else_stmt, self.curtok.line)

    def while_stmt(self):
        expr = self.cond_stmt("while")
        block = self.block_stmt()
        return WhileNode(expr, block, self.curtok.line)

    def statement(self):
        val = self.curtok.literal
        if val == "print" or val == "println":
            return self.print_stmt(val)
        elif val == "check":
            return self.if_stmt()
        elif val == "while":
            return self.while_stmt()
        elif val in ("continue", "break"):
            line = self.curtok.line
            self.advance()
            return FlowNode(val, line)
        else:
            return self.assignment()

    def block_stmt(self):
        statements = []
        while self.curtok.literal != "end":
            if self.curtok.type == tokenizer.EOF:
                raise ParserException(self.curtok.line, "end", "ex")
            statements.append(self.statement())
        self.advance()
        return statements
    
    def program(self):
        statements = []
        while self.curtok.type != tokenizer.EOF:
            statements.append(self.statement())
        return statements
from exceptions import ParserException
import parse.tokenizer as tokenizer
# Parser

# Node types
class NumNode:
    def __init__(self,val,line):
        self.val = val
        self.line = line
    def __repr__(self):
        return str(self.val)

class StringNode:
    def __init__(self,val,line):
        self.val = val
        self.line = line
    def __repr__(self):
        return f'\"{self.val}\"'

class BooleanNode:
    def __init__(self, val, line):
        self.val = val
        self.line = line
    def __repr__(self):
        return f'{"true" if self.val == 1 else "false"}'


class BinaryOpNode:
    def __init__(self,left,op,right,line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
    def __repr__(self):
        return f'({str(self.left)} {str(self.op)} {str(self.right)})'

class UnaryOpNode:
    def __init__(self,op,node,line):
        self.op = op
        self.node = node
        self.line = line
    def __repr__(self):
        return f'{self.op}{self.node}'


class VAssignmentNode:
    def __init__(self,expr,id,line):
        self.expr = expr
        self.id = id
        self.line = line
    def __repr__(self):
        return f'[{self.expr} -> {self.id}]'

class VAccessNode:
    def __init__(self, id, line):
        self.id = id
        self.line = line
    def __repr__(self):
        return f'[{self.id}]'


class CheckNode:
    def __init__(self, expr, block, line):
        self.expr = expr
        self.block = block
        self.line = line
    def __repr__(self):
        return f'CHECK[{self.expr}]: {self.block}'

class ElseNode:
    def __init__(self, block, line):
        self.block = block
        self.line = line
    def __repr__(self):
        return f'ELSE[{self.block}]'

class WhileNode:
    def __init__(self, expr, block, line):
        self.expr = expr
        self.block = block
        self.line = line
    def __repr__(self):
        return f'WHILE[{self.expr}]: {self.block}'

class PrintNode:
    def __init__(self, expr, line, println):
        self.expr = expr
        self.line = line
        self.println = println
    def __repr__(self):
        return f'PRINT{"LN" if self.println else ""}[{self.expr}]'
        
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
    
    def advance(self):
        self.index+=1
        if self.index < len(self.tokens):
            self.curtok = self.tokens[self.index]
        return self.curtok

    def consume(self,type,token):
        if self.curtok.type == type and self.curtok.literal == token:
            self.advance()
            return True
        else: raise ParserException(self.curtok.line,token,"expected")
    
    def bin_op(self,func,ops):
        l = func()
        while self.curtok.literal in ops and not self.curtok.literal == "":
            op = self.curtok.literal
            self.advance()
            r = func()
            l = BinaryOpNode(l,op,r,self.curtok.line)
        return l

    def cond_stmt(self,key):
        self.consume(tokenizer.KEY,key)
        self.consume(tokenizer.L_BRACKET,'[')
        expr = self.l_expr()
        self.consume(tokenizer.R_BRACKET,']')
        self.consume(tokenizer.B_BLCK,':')
        return expr

    # Productions
    def factor(self):
        tok = self.curtok
        if tok.type == tokenizer.NUM:
            self.advance()
            return NumNode(tok.literal,self.curtok.line)
        # TODO: Expand on this later to include function definitons and such
        elif tok.type == tokenizer.ID:
            self.advance()
            return VAccessNode(tok.literal,self.curtok.line)
        elif tok.type == tokenizer.EOF:
            raise ParserException(self.curtok,"EOF","unex")
        elif tok.literal == "true" or tok.literal == "false":
            self.advance()
            return BooleanNode(1 if tok.literal == "true" else 0, self.curtok.line)
        elif tok.type == tokenizer.STR:
            str = self.curtok.literal
            self.advance()
            return StringNode(str,self.curtok.line)
        elif tok.literal in ("+", "-"):
            op = tok.literal
            self.advance()
            return UnaryOpNode(op,self.factor(),self.curtok.line)
        elif tok.literal == '(':
            self.advance()
            expr = self.a_expr()
            if self.curtok.literal == ')':
                self.advance()
                return expr
            else:
                raise ParserException(tok.line,"Expected ')'")
        else: raise ParserException(tok.line, tok.literal, "unex")

    def term(self):
        return self.bin_op(self.factor,("*","/","%"))

    def a_expr(self):
        return self.bin_op(self.term,("+","-"))

    def l_expr(self):
        if self.curtok.literal == '!':
            self.advance()
            return UnaryOpNode("!", self.l_expr(), self.curtok.line)
        else:
            return self.bin_op(self.a_expr,("=","!=","<=",">=","<",">"))

    def assignment(self):
        expr = self.l_expr()
        if self.curtok.type == tokenizer.ASSIGN:
            self.advance()
            id = self.factor()
            if isinstance(id,VAccessNode):
                return VAssignmentNode(expr, id.id, self.curtok.line)
            else:
                raise ParserException(self.curtok.line,"Identifier", "ex")
        else: return expr

    def print_stmt(self, key):
        self.advance()
        expr = self.l_expr()
        return PrintNode(expr,self.curtok.line, True if key == "println" else False)

    def else_stmt(self):
        pass

    def ifelse_stmt(self):
        pass

    def if_stmt(self):
        expr = self.cond_stmt("check")
        block = self.block_stmt()
        return CheckNode(expr,block,self.curtok.line)

    def while_stmt(self):
        expr = self.cond_stmt("while")
        block = self.block_stmt()
        return WhileNode(expr,block,self.curtok.line)

    def statement(self):
        val = self.curtok.literal
        if val == "print" or val == "println": return self.print_stmt(val)
        elif val == "check": return self.if_stmt()
        elif val == "while": return self.while_stmt()
        elif val in ('\n', '\r\n'): self.advance()
        else: return self.assignment()


    def block_stmt(self):
        statements = []
        while not self.curtok.literal == "end":
            if self.curtok.type == tokenizer.EOF:
                raise ParserException(self.curtok.line,"end","ex")
            if not self.curtok.type == tokenizer.NL:
                statements.append(self.statement())
            self.advance()
        return statements
    
    def program(self):
        statements = []
        while not self.curtok.type == tokenizer.EOF:
            if not self.curtok.type == tokenizer.NL:
                statements.append(self.statement())
            self.advance()
        return statements

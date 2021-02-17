# Nodes for AST
# Data types
class NumNode:
    def __init__(self, val, line):
        self.val = val
        self.line = line
    def __repr__(self):
        return str(self.val)

class StringNode:
    def __init__(self, val, line):
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

# Operations
class BinaryOpNode:
    def __init__(self, left, op, right, line):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
    def __repr__(self):
        return f'({str(self.left)} {str(self.op)} {str(self.right)})'

class UnaryOpNode:
    def __init__(self, op, node, line):
        self.op = op
        self.node = node
        self.line = line
    def __repr__(self):
        return f'{self.op}{self.node}'

# Variables
class AssignmentNode:
    def __init__(self, expr, id, line):
        self.expr = expr
        self.id = id
        self.line = line
    def __repr__(self):
        return f'[{self.expr} -> {self.id}]\n'

class AccessNode:
    def __init__(self, id, line):
        self.id = id
        self.line = line
    def __repr__(self):
        return f'[{self.id}]'

# Control flow
class CheckNode:
    def __init__(self, expr, block, celse_stmts, else_stmt, line):
        self.expr = expr
        self.block = block
        self.celse_stmts = celse_stmts
        self.else_stmt = else_stmt
        self.line = line
    def __repr__(self):
        str_else = self.else_stmt if self.else_stmt != None else ""
        return f'CHECK[{self.expr}]:\n {self.block}\n {self.celse_stmts}\n {str_else}'

class CelseNode:
    def __init__(self, expr, block, line):
        self.expr = expr
        self.block = block
        self.line = line
    def __repr__(self):
        return f'CELSE[{self.expr}]:\n {self.block}\n'

class ElseNode:
    def __init__(self, block, line):
        self.block = block
        self.line = line
    def __repr__(self):
        return f'ELSE:\n{self.block}\n'

class WhileNode:
    def __init__(self, expr, block, line):
        self.expr = expr
        self.block = block
        self.line = line
    def __repr__(self):
        return f'WHILE[{self.expr}]:\n {self.block}\n'

class FlowNode:
    def __init__(self, key, line):
        self.key = key
        self.line = line
    def __repr__(self):
        if self.key == "continue":
            return "CONTINUE"
        elif self.key == "break":
            return "BREAK"

# Print
class PrintNode:
    def __init__(self, expr, line, println):
        self.expr = expr
        self.line = line
        self.println = println
    def __repr__(self):
        return f'PRINT{"LN" if self.println else ""}[{self.expr}]\n'

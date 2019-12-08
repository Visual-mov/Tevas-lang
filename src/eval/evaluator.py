import sys
import eval.types as types
from exceptions import RunTimeException
import parse.parser as parser

# Symbol Table
class SymbolTable:
    def __init__(self, parent=None):
        self.list = {}
        self.parent = parent

    def put(self, key, value):
        self.list[key] = value

    def lookup(self, key):
        val = self.list.get(key, None)
        if val == None and not self.parent == None:
            return self.parent.lookup(key)
        else: return val

    def remove(self, key):
        del list[key] 
        
class Evaluator:
    def __init__(self,tree,gTable):
        self.tree = tree
        self.gTable = gTable
    
    def eval(self):
        for node in self.tree:
            self.visit(node)

    def check_type(self,l,r,type):
        return isinstance(l,type) and isinstance(r,type)

    def visit(self,node):
        return getattr(self, f'v_{type(node).__name__}', self.v_Unknown)(node)
    
    def v_BinaryOpNode(self, node):
        r = self.visit(node.right)
        l = self.visit(node.left)

        if self.check_type(l,r,types.Float):
            if node.op == '+':
                return types.Float(l.add(r))
            elif node.op == '-':
                return types.Float(l.minus(r))
            elif node.op == '/':
                if r.val == 0:
                    raise RunTimeException(node.line,"Division by 0.")
                return types.Float(l.divide(r))
            elif node.op == '*':
                return types.Float(l.multiply(r))
            elif node.op == '%':
                return types.Float(l.modulo(r))
        if node.op == '=':
            return types.Boolean(1 if l.val == r.val else 0)
        elif node.op == '<':
            return types.Boolean(1 if l.val < r.val else 0)
        elif node.op == '<=':
            return types.Boolean(1 if l.val <= r.val else 0)
        elif node.op == '>':
            return types.Boolean(1 if l.val > r.val else 0)
        elif node.op == '>=':
            return types.Boolean(1 if l.val >= r.val else 0)
        elif node.op == '!=':
            return types.Boolean(1 if not l.val == r.val else 0)

        raise RunTimeException(node.line,"Can not apply arithmetical operations on " + type(l).__name__ + " and " + type(r).__name__)

    def v_UnaryOpNode(self, node):
        if node.op == '-':
            return types.Float(self.visit(node.node).val).negate()
        elif node.op == '+':
            return types.Float(self.visit(node.node).val).abs()
        elif node.op == '!':
            return types.Boolean(self.visit(node.node).val).Not()

    def v_NumNode(self, node):
        return types.Float(node.val)
    
    def v_BooleanNode(self, node):
        return types.Boolean(node.val)

    def v_StringNode(self, node):
        return types.String(node.val)

    def v_VAssignmentNode(self, node):
        val = self.visit(node.expr)
        self.gTable.put(node.id,val)
        return val

    def v_VAccessNode(self, node):
        var = self.gTable.lookup(node.id)
        if var == None:
            raise RunTimeException(node.line,f'"{node.id}" is not defined.')
        return var
    
    def v_PrintNode(self, node):
        val = self.visit(node.expr)
        sys.stdout.write(val.get_literal() + ('\n' if node.println else ""))

    def v_CheckNode(self,node):
        expr = self.visit(node.expr)
        if expr.val == 1:
            for statement in node.block:
                self.visit(statement)
    
    def v_WhileNode(self, node):
        while self.visit(node.expr).val == 1:
            for statement in node.block:
                self.visit(statement)

        
    def v_Unknown(self, node): 
        raise RunTimeException(0,"Unknown node type.") #TODO Get line number via other method. Overhall method for transfering line number.

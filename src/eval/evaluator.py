import sys
import eval.types as types
from exceptions import RunTimeException
import parse.parser as parser

# Evaluator

# Context
class Scope:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.table = SymbolTable(parent)

# Symbol Table
class SymbolTable:
    def __init__(self, parent=None):
        self.list = {}
        self.parent = parent

    def put(self, key, value):
        self.list[key] = value

    def lookup(self, key):
        val = self.list.get(key, None)
        if val == None and self.parent != None:
            return self.parent.lookup(key)
        else: return val

    def remove(self, key):
        del list[key] 
        
class Evaluator:
    def __init__(self,tree,g_scope):
        self.tree = tree
        self.scope_stack = []
        self.scope_stack.append(g_scope)
    
    def eval(self):
        for node in self.tree:
            self.visit(node)
    
    def visit(self,node):
        return getattr(self, f'v_{type(node).__name__}', self.v_Unknown)(node)

    def check_type(self,l,r,type=None):
        if type == None: return isinstance(l,r)
        else: return isinstance(l,type) and isinstance(r,type)

    def add_scope(self, scope):
        scope.parent = self.scope_stack[len(self.scope_stack) - 1]
        self.scope_stack.append(scope)
    
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
            return types.Boolean(1 if l.val != r.val else 0)
        
        if node.op == "&&":
            return l.And(r)
        if node.op == "||":
            return l.Or(r)

        raise RunTimeException(node.line,"Can not apply arithmetical operations on " + type(l).__name__ + " and " + type(r).__name__)

    def v_UnaryOpNode(self, node):
        val = self.visit(node.node)

        if self.check_type(val,types.Float):
            if node.op == '-':
                return types.Float(val.val).negate()
            elif node.op == '+':
                return types.Float(val.val).abs()

        if node.op == '!' and self.check_type(val,types.Boolean):
            return types.Boolean(val.val).Not()
        else: raise RunTimeException(node.line,"Can not apply logical operations on " + type(val).__name__)

    def v_NumNode(self, node):
        return types.Float(node.val)
    
    def v_BooleanNode(self, node):
        return types.Boolean(node.val)

    def v_StringNode(self, node):
        return types.String(node.val)

    def v_VAssignmentNode(self, node):
        val = self.visit(node.expr)
        self.scope_stack[0].table.put(node.id,val)
        return val

    def v_VAccessNode(self, node):
        var = self.scope_stack[0].table.lookup(node.id)
        if var == None:
            raise RunTimeException(node.line,f'"{node.id}" is not defined.')
        return var
    
    def v_PrintNode(self, node):
        val = self.visit(node.expr)
        sys.stdout.write(val.get_literal() + ('\n' if node.println else ""))

    def v_FlowNode(self, node):
        print(node)

    def v_CheckNode(self,node):
        visit_else = True
        val = self.visit(node.expr)
        if self.check_type(val, types.Boolean):
            if val.val == 1:
                for statement in node.block:
                    visit_else = False
                    self.visit(statement)
            elif val.val == 0 and node.celse_stmts != None:
                for celse_stmt in node.celse_stmts:
                    if self.visit(celse_stmt.expr).val == 1:
                        visit_else = False
                        for statement in celse_stmt.block:
                            visit_else = False
                            self.visit(statement)
            if visit_else and node.else_stmt != None:
                for statement in node.else_stmt.block:
                    self.visit(statement)
        else: raise RunTimeException(node.line,"Expression must be of type Boolean.")

    def v_WhileNode(self, node):
        while self.visit(node.expr).val == 1:
            for statement in node.block:
                self.visit(statement)

    def v_Unknown(self, node): 
        raise RunTimeException(0,"Unknown node type.") #TODO Get line number via other method. Overhall method for transfering line number.

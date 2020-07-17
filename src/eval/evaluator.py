import sys
import eval.types as types
from exceptions import RunTimeException
import parse.parser as parser

# Symbol Table
# The symbol table is used for storing variables and their values.
# No logic exists to check for tables in a higher context, as tex
# programs only have one scope.
class SymbolTable:
    def __init__(self):
        self.list = {}

    def put(self, key, value):
        self.list[key] = value

    def lookup(self, key):
        return self.list.get(key, None)

    def remove(self, key):
        del self.list[key] 

# Evaluator class
# Executes syntax tree. Stores all the actual rules and "logic" of the language.
class Evaluator:
    def __init__(self, tree, g_table, print_vars):
        self.tree = tree
        self.g_table = g_table
        self.print_vars = print_vars
        self.do_break = False
        self.do_continue = False
    
    def eval(self):
        for node in self.tree:
            val = self.visit(node)
            if val != None and self.print_vars:
                print(val.get_literal())

    def check_type(self, l, r, type=None):
        if type == None: return isinstance(l, r)
        else: return isinstance(l, type) and isinstance(r, type)

    def check_either(self, l, r, type):
        return self.check_type(l, type) or self.check_type(r, type)

    # Visit methods
    def visit(self, node):
        return getattr(self, f'v_{type(node).__name__}', self.v_Unknown)(node)
    
    def v_BinaryOpNode(self, node):
        r = self.visit(node.right)
        l = self.visit(node.left)

        if self.check_type(l, r, types.Float):
            if r.val == 0 and node.op == '/':
                raise RunTimeException(node.line, "Division by 0")
            if r.val == 0 and node.op == '%':
                raise RunTimeException(node.line, "Modulo by 0")
            float_ops = {
                "+": types.Float(l.add(r)), 
                "-": types.Float(l.minus(r)), 
                "*": types.Float(l.multiply(r)), 
                "/": types.Float(l.divide(r)) if r.val != 0 else 0, 
                "%": types.Float(l.modulo(r)) if r.val != 0 else 0, 

                "<": types.Boolean(1 if l.val < r.val else 0), 
                "<=": types.Boolean(1 if l.val <= r.val else 0), 
                ">": types.Boolean(1 if l.val > r.val else 0), 
                ">=": types.Boolean(1 if l.val >= r.val else 0)
            }
            if node.op in float_ops.keys():
                return float_ops[node.op]

        if self.check_type(l, r, types.Boolean):
            if node.op == "&&":
                return l.And(r)
            elif node.op == "||":
                return l.Or(r)
        
        if node.op == "=":
            return types.Boolean(1 if l.val == r.val else 0)
        elif node.op == "!=":
            return types.Boolean(1 if l.val != r.val else 0)

        if node.op == '+' and self.check_either(r, l, types.String):
            if not self.check_either(r, l, types.Boolean):
                return types.String(types.String(str(l.val)).append_string(r.val))
            else: raise RunTimeException(node.line, "Can not add Boolean to compound String")

        raise RunTimeException(node.line, "Can not apply arithmetical operations on " + type(l).__name__ + " and " + type(r).__name__)

    def v_UnaryOpNode(self, node):
        val = self.visit(node.node)
        if self.check_type(val, types.Float):
            if node.op == '-':
                return types.Float(val.val).negate()
            elif node.op == '+':
                return types.Float(val.val).absolute()

        if node.op == '!' and self.check_type(val, types.Boolean):
            return types.Boolean(val.val).Not()
        else:
            raise RunTimeException(node.line, "Can not apply logical operations on " + type(val).__name__)

    def v_NumNode(self, node):
        return types.Float(node.val)
    
    def v_BooleanNode(self, node):
        return types.Boolean(node.val)

    def v_StringNode(self, node):
        return types.String(node.val)

    def v_VAssignmentNode(self, node):
        val = self.visit(node.expr)
        self.g_table.put(node.id, val)
        return val

    def v_VAccessNode(self, node):
        var = self.g_table.lookup(node.id)
        if var == None:
            raise RunTimeException(node.line, f'"{node.id}" is not defined')
        return var
    
    def v_PrintNode(self, node):
        val = self.visit(node.expr)
        sys.stdout.write(val.get_literal() + ('\n' if node.println else ""))

    def v_FlowNode(self, node):
        if node.key == "break":
            self.do_break = True
        elif node.key == "continue":
            self.do_continue = True

    def v_CheckNode(self, node):
        visit_else = True
        val = self.visit(node.expr)
        if self.check_type(val, types.Boolean):
            if val.val == 1:
                visit_else = False
                for statement in node.block:
                    if True not in (self.do_break, self.do_continue): self.visit(statement)

            elif val.val == 0 and node.celse_stmts != None:
                for celse_stmt in node.celse_stmts:
                    if self.visit(celse_stmt.expr).val == 1:
                        visit_else = False
                        for statement in celse_stmt.block:
                            if True not in (self.do_break, self.do_continue): self.visit(statement)

            if visit_else and node.else_stmt != None:
                for statement in node.else_stmt.block:
                    if True not in (self.do_break, self.do_continue): self.visit(statement)
        else:
            raise RunTimeException(node.line, "Expression must be of type Boolean")

    def v_WhileNode(self, node):
        while self.visit(node.expr).val == 1 and not self.do_break:
            for statement in node.block:
                if self.do_continue or self.do_break: break
                self.visit(statement)
            if self.do_continue:
                self.do_continue = False
                continue
        self.do_break = False
        self.do_continue = False

    def v_Unknown(self, node): 
        raise RunTimeException(0, "Unknown node type")

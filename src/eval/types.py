from parse.parser import NumNode

#! __repr__ ONLY USED FOR DEBUGGING

class Float:
    def __init__(self,val):
        self.val = val
    
    def add(self, node):
        return self.val + node.val
    def minus(self, node):
        return self.val - node.val
    def divide(self, node):
        return self.val / node.val
    def multiply(self, node):
        return self.val * node.val
    def modulo(self, node):
        return self.val % node.val

    def negate(self): return Float(self.multiply(Float(-1)))
    def abs(self): return Float(abs(self.val))

    def get_literal(self):
        return self.val
    def __repr__(self):
        return f'FLOAT: {self.val}'

class String:
    def __init__(self,val):
        self.val = val
    
    def add_string(self,str1):
        self.val += str1

    def get_literal(self):
        return self.val
    def __repr__(self):
        return f'STRING: {self.val}'

class Boolean:
    def __init__(self,val):
        self.val = val
    
    def And(self,bool):
        return Boolean(1 if self.val == 1 and bool.val == 1 else 0)
    def Or(self,bool):
        return Boolean(1 if self.val == 1 or bool.val == 1 else 0)
    def Not(self):
        return Boolean(1 if self.val == 0 else 0)
    
    def get_literal(self):
        return "true" if self.val == 1 else "false"
    def __repr__(self):
        return f'BOOL: {"true" if self.val == 1 else "false"}'
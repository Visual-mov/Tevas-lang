from parse.parser import NumNode

#! __repr__ ONLY USED FOR DEBUGGING

class Type:
    def __init__(self, val):
        self.val = val
    def get_literal(self):
        return str(self.val)

class Float(Type):
    def __init__(self,val):
        super().__init__(val)
    
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

    def __repr__(self):
        return f'FLOAT: {self.val}'

class String(Type):
    def __init__(self,val):
        super().__init__(val)
    
    def append_string(self,str1):
        return self.val + str(str1)

    def __repr__(self):
        return f'STRING: {self.val}'

class Boolean(Type):
    def __init__(self,val):
        super().__init__(val)
    
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
class TevasException:
    def __init__(self, line, errtype, message):
        self.line = line
        self.message = message
        print(u"\u001b[31m" + f'Line {line}: {errtype}.\n > {message}.' + u"\u001b[0m")
        exit()
    
class LexerException(TevasException):
    def __init__(self, line, message):
        super().__init__(line, "Lex Error", message)

class ParserException(TevasException):
    def __init__(self, line, message="", type=""):
        if type == "ex":
            message = f"Expected '{message}' token"
        elif type == "unex":
            message = f"Unexpected '{message}' token"
        super().__init__(line, "Parse error", message)
        
class RunTimeException(TevasException):
    def __init__(self, line, message):
        super().__init__(line, "Tevas Runtime error", message)
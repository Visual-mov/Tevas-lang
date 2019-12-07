class TexExeption:
    def __init__(self,line, errtype, message):
        self.line = line
        self.message = message
        execption = f'Line {line}: {errtype}: {message}'
        print(u"\u001b[31m" + execption + u"\u001b[0m")
        exit()
    
class LexerException(TexExeption):
    def __init__(self,line,message):
        super().__init__(line, "Lex Error", message)

class ParserException(TexExeption):
    def __init__(self,line,message="",type=""):
        if type == "ex": message = f"Expected '{message}' token."
        elif type == "unex": message = f"Unexpected '{message}' token."
        super().__init__(line, "Parse error", message)
        
class RunTimeException(TexExeption):
    def __init__(self,line,message):
        super().__init__(line, "Tex Runtime error", message)
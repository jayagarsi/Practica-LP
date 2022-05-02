import sys
from CodeAndAudioGenerator import *
from JSBachVisitor import *

class jsbachExceptions(Exception):

    def __init__(self, message):
        self.message = "Error: " + message

def main():
    if len(sys.argv) != 2:
        print("Error: no ha introduit cap fitxer")
    else:

        input_stream = FileStream(sys.argv[1])

        lexer = jsbachLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = jsbachParser(token_stream)
        tree = parser.program()
        #if lexer.getNumberOfSyntaxErrors() > 0 or parser.getNumberOfSyntaxErrors() > 0:
        #    print("Lexical and/or syntactical errors have been found.")
        #else:    
        
        visitor = TreeVisitor()

        try:
            visitor.visit(tree)
        except jsbachExceptions as e:
            print(e.message)

        notesString = visitor.getNotesString()
        if notesString == "":
            print("Not generating any midi, wav or mp3 file as there is no song to play")
        else:
            fileName = 'musica'
            codeGen = CodeAndAudioGenerator(fileName, notesString)
            codeGen.executeFileCreation()

if __name__ == "__main__":
    main()
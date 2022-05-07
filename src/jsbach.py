import sys
from CodeAndAudioGenerator import *
from JSBachVisitor import *


def main():
    if len(sys.argv) < 1:
        print("Error: no file has been introduced")
    else:
        firstFunctionName = "Main"
        firstFunctionParams = []
        if len(sys.argv) == 3:
            firstFunctionName = sys.argv[2]
            firstFunctionParams = []
        elif len(sys.argv) >= 4:
            firstFunctionName = sys.argv[2]
            firstFunctionParams = sys.argv[3:]

        for i in range(len(firstFunctionParams)):
            firstFunctionParams[i] = int(firstFunctionParams[i])

        input_stream = FileStream(sys.argv[1])

        lexer = jsbachLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = jsbachParser(token_stream)
        parser.addErrorListener(MyErrorListener())

        tree = parser.program()
        visitor = TreeVisitor(firstFunctionName, firstFunctionParams)

        try:
            visitor.visit(tree)
            notesString = visitor.getNotesString()
            if notesString == "":
                print("Not generating any midi, wav or mp3 file as there is no song to play")
            else:
                fileName = 'musica'
                codeGen = CodeAndAudioGenerator(fileName, notesString)
                codeGen.executeFileCreation()

        except jsbachExceptions as e:
            print(e.message)

if __name__ == "__main__":
    main()

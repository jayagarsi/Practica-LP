from CodeAndAudioGenerator import *
from MyJSBachVisitor import *


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 jsbach.py program.jsb [functionname] [parameters]")
    else:
        programName = sys.argv[1]
        fileName = os.path.basename(programName)
        n = len(fileName) - 4
        extension = fileName[-3:]
        if extension != "jsb":
            print("ERROR: expecting file with .jsb extention and recieved ." + extension)
            sys.exit()
        fileName = fileName[0:n]

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

        input_stream = FileStream(sys.argv[1], encoding='utf-8')

        lexer = jsbachLexer(input_stream)
        lexer.addErrorListener(jsbachErrorListener())
        token_stream = CommonTokenStream(lexer)
        parser = jsbachParser(token_stream)
        parser.addErrorListener(jsbachErrorListener())

        tree = parser.program()
        visitor = TreeVisitor(firstFunctionName, firstFunctionParams)

        try:
            visitor.visit(tree)
            notesString = visitor.getNotesString()
            if notesString == "":
                print("Not generating any midi, wav or mp3 file as there is no song to play")
            else:
                tempo = visitor.getNotesTempo()
                key = visitor.getKeySignature()
                compas = visitor.getCompasTime()

                codeGen = CodeAndAudioGenerator(fileName, notesString, tempo, key, compas)
                codeGen.executeFileCreation()

        except jsbachExceptions as e:
            print(e.message)

if __name__ == "__main__":
    main()

import sys
import os
from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from jsbachVisitor import jsbachVisitor


class TreeVisitor(jsbachVisitor):

    def __init__(self, SymbolTable, notesString):
        self.SymbolTable = {}
        self.notesString = ""

    def getNotesString(self):
        return self.notesString

    def visitMain(self, ctx):
        self.visit(ctx.statements())

    def visitParamstring(self, ctx):
        chd = list(ctx.getChildren())
        return chd[0].getText()

    def visitAssignStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        exp = self.visit(chd[2])
        self.SymbolTable[id] = exp

    def visitIfStmt(self, ctx):
        chd = list(ctx.getChildren())
        expr = self.visit(chd[1])
        if expr:
            self.visit(chd[3])
        else:
            if len(chd) > 5:
                self.visit(chd[7])

    def visitWhileStmt(self, ctx):
        chd = list(ctx.getChildren())
        expr = self.visit(chd[1])
        while expr:
            self.visit(chd[3])
            expr = self.visit(chd[1])

    def visitReadStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[1].getText()
        self.SymbolTable[id] = input()

    def visitWriteStmt(self, ctx):
        chd = list(ctx.getChildren())
        for i in range(1, len(chd)):
            val = self.visit(chd[i])
            print(val)

    def visitPlayStmt(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[1])

    def visitParenthesis(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[1])

    def visitUnary(self, ctx):
        op, expr = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val = self.visit(expr)
        if op == "PLUS":
            return val
        else:
            return -val

    def visitArithmetic(self, ctx):
        expr1, op, expr2 = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        val2 = self.visit(expr2)
        if op == "MUL":
            return val1 * val2
        elif op == "DIV":
            return val1 // val2
        elif op == "MOD":
            return val1 % val2
        elif op == "PLUS":
            return val1 + val2
        else:
            return val1 - val2

    def visitRelational(self, ctx):
        expr1, op, expr2 = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        val2 = self.visit(expr2)
        if op == "EQU":
            if val1 == val2:
                return 1
            else:
                return 0
        elif op == "NEQ":
            if val1 != val2:
                return 1
            else:
                return 0
        elif op == "LET":
            if val1 < val2:
                return 1
            else:
                return 0
        elif op == "LEQ":
            if val1 <= val2:
                return 1
            else:
                return 0
        elif op == "GET":
            if val1 > val2:
                return 1
            else:
                return 0
        else:
            if val1 >= val2:
                return 1
            else:
                return 0

    def visitValue(self, ctx):
        val = list(ctx.getChildren())
        if len(val) > 1:
            return self.visit(val[0])
        else:
            return int(val[0].getText())
    
    def visitArratype(self, ctx):
        chd = list(ctx.getChildren())
        l = []
        for i in chd:
            if i != ',' and i != '{' and i != '}':
                l += self.visit(i)
        return l

    def visitNotes(self, ctx):
        chd = list(ctx.getChildren())
        note = chd[0].getText()
        snote = ord(str(note[0]))
        snote = snote + 32
        snote = chr(snote)
        notesToValues = {"A" : 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 4*8
            snote = snote + "'4"
        else:
            offset = int(note[1])*8          # les notes van de 8 en 8
            snote = snote + "'" + str(note[1])

        snote = str(snote) + " "
        self.notesString += snote
        print(self.notesString)
        val = note[0]
        return notesToValues[val]+offset

    def visitExprIdent(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[0])

    def visitVarident(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        if id not in self.SymbolTable:
            self.SymbolTable[id] = 0
        return int(self.SymbolTable[id])

    def visitFuncident(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        if id not in self.SymbolTable:
            self.SymbolTable[id] = 0
        return id

class FileConverterManager():
    def __init__(self, fN, notesS):
        self.fileName = fN
        self.lilyFileName = self.fileName + ".lily"
        self.notesString = notesS

    def executeFileCreation(self):
        self.writeLilyPondFile()
        self.generatePDFandMidiFiles()
        self.generateWAVFile()
        self.generateMP3File()

    def writeLilyPondFile(self):
        file_object = open(self.lilyFileName, 'w')
        file_object.write("\\version \"2.20.0\" \n")
        file_object.write("\\score {\n")
        file_object.write("   \\absolute { \n")
        file_object.write("        \\tempo 4 = 120 \n")

        s = "         " + self.notesString + " \n"
        file_object.write(s)

        file_object.write("   } \n")
        file_object.write("   \\layout { } \n")
        file_object.write("   \\midi { } \n")
        file_object.write("}")
        file_object.close()

    def generatePDFandMidiFiles(self):
        print("----- GENERATING PDF AND MIDI FILES -----")
        lilyPondInstruction = "lilypond " + self.lilyFileName
        os.system(lilyPondInstruction)
        print("----- SUCCESSFULLY GENERATED PDF AND MIDI FILES ----- \n")

    def generateWAVFile(self):
        print("----- GENERATING WAV FILE -----")
        wavInstruction = "timidity -Ow -o " + self.fileName + ".wav " + self.fileName + ".midi" 
        os.system(wavInstruction)
        print("----- SUCCESSFULLY GENERATED WAV FILE ----- \n")
    
    def generateMP3File(self):
        mp3FilePath = "./" + self.fileName + ".mp3"
        if os.path.exists(mp3FilePath):
            os.remove(mp3FilePath)
            
        print("----- GENERATING MP3 FILE -----")
        wavInstruction = "ffmpeg -i " + self.fileName + ".wav -codec:a libmp3lame -qscale:a 2 " + self.fileName + ".mp3"
        os.system(wavInstruction)
        print("----- SUCCESSFULLY GENERATED MP3 FILE -----")

def main():
    if len(sys.argv) != 2:
        print("Error: no ha introduit cap fitxer")
    else:

        input_stream = FileStream(sys.argv[1])

        lexer = jsbachLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = jsbachParser(token_stream)

        #if lexer.getNumberOfSyntaxErrors() > 0 or parser.getNumberOfSyntaxErrors() > 0:
        #    print("Lexical and/or syntactical errors have been found.")
        #else:    

        tree = parser.program()
        
        SymbolTable = {}
        notesString = ""
        visitor = TreeVisitor(SymbolTable, notesString)
        visitor.visit(tree)

        notesString = visitor.getNotesString()
        if notesString == "":
            print("Not generating any midi, wav or mp3 file as there is no song to play")
        else:
            fileName = 'musica'
            fileManager = FileConverterManager(fileName, notesString)
            fileManager.executeFileCreation()

if __name__ == "__main__":
    main()
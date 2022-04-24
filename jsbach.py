import sys
import re
from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from jsbachVisitor import jsbachVisitor


class TreeVisitor(jsbachVisitor):

    def __init__(self, SymbolTable):
        self.SymbolTable = {}

    def visitProgram(self, ctx):
        chd = list(ctx.getChildren())
        for i in chd:
            self.visit(i)

    def visitMain(self, ctx):
        chd = list(ctx.getChildren())
        self.visit(chd[2])

    def visitParamstring(self, ctx):
        chd = list(ctx.getChildren())
        return chd[0].getText()

    def visitAssignStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        exp = self.visit(chd[2])
        SymbolTable[id] = exp

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
        SymbolTable[id] = input()

    def visitWriteStmt(self, ctx):
        chd = list(ctx.getChildren())
        for i in range(1, len(chd)):
            val = self.visit(chd[i])
            print(val)

    def visitPlayStmt(self, ctx):
        chd = list(ctx.getChildren())

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
        return int(val[0].getText())
    
    def visitNotes(self, ctx):
        chd = list(ctx.getChildren())
        note = chd[0].getText()
        notesToValues = {"A" : 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 4*8
        else:
            offset = int(note[1])*8          # les notes van de 8 en 8

        val = note[0]
        return notesToValues[val]+offset

    def visitExprIdent(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[0])

    def visitVarident(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        if id not in SymbolTable:
            SymbolTable[id] = 0
        return int(SymbolTable[id])

    def visitFuncident(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        if id not in SymbolTable:
            SymbolTable[id] = 0
        return id

def openLilyPondFile():
    file_object = open('musica.lily', 'a')
    file_object.write("\\version \"2.22.1\" \n")
    file_object.write("\\score {\n")
    file_object.write("   \\absolute { \n")
    file_object.write("        \\tempo 4 = 120 \n")
    file_object.close()


def closeLilyPondFile():
    file_object = open('musica.lily', 'a')
    file_object.write("   } \n")
    file_object.write("   \\layout { } \n")
    file_object.write("   \\midi { } \n")
    file_object.write("}")
    file_object.close()

def generatePDFandMidiFiles():
    file_object = open('musica.lily', 'a')
    file_object.close()

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
    openLilyPondFile()

    tree = parser.program()
    
    SymbolTable = {}
    visitor = TreeVisitor(SymbolTable)
    visitor.visit(tree)

    closeLilyPondFile()
    generatePDFandMidiFiles()

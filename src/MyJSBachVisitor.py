import sys
from antlr4 import *
from jsbachVisitor import jsbachVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from antlr4.error.ErrorListener import ErrorListener
from itertools import dropwhile
from random import randint


class jsbachErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("ERROR: there are some syntactical or lexical errors")
        sys.exit()

class jsbachExceptions(Exception):
    def __init__(self, message):
        self.message = "ERROR: " + message

class jsbachFunctionInfo():
    def __init__(self, name, params, context):
        self.name = name
        self.params = params
        self.context = context

class TreeVisitor(jsbachVisitor):
    def __init__(self, firstFunctionName="", firstFunctionParams=[]):
        self.Procedures = {}
        self.SymbolTable = []
        self.notesString = ""
        self.actualScope = 0
        self.firstFunction = firstFunctionName
        self.firstParams = firstFunctionParams
        self.tempo = 120
        self.key = ""
        self.compas = ""

    def getNotesString(self):
        return self.notesString

    def getNotesTempo(self):
        return self.tempo

    def getKeySignature(self):
        return self.key

    def getCompasTime(self):
        return self.compas

    # ------------------- PROCEDURES RULE ------------------ #

    def visitProcedures(self, ctx):
        chd = list(ctx.getChildren())
        for proc in chd:
            procid = proc.PROCID().getText()
            if procid in self.Procedures:
                msg = "Already existin function with name "
                msg += procid
                raise jsbachExceptions(msg)
            Func = jsbachFunctionInfo(procid, proc.parameters(), proc.statements())
            self.Procedures[procid] = Func

        if self.firstFunction != "":
            if self.firstFunction not in self.Procedures:
                if "Main" not in self.Procedures:
                    msg = "Trying to execute a non existing procedure named "
                    msg += self.firstFunction
                    msg += " in a program without Main"
                    raise jsbachExceptions(msg)
                else:
                    Func = self.Procedures["Main"]
            else:
                Func = self.Procedures[self.firstFunction]
        else:
            if "Main" not in self.Procedures:
                raise jsbachExceptions("Trying to execute a program without a Main procedure")
            else:
                Func = self.Procedures["Main"]
        Scope = {}
        self.SymbolTable.append(Scope)
        funcParams = self.visit(Func.params)

        if len(funcParams) != len(self.firstParams):
            msg = "Passed parameters don't match with parameters in " + Func.name
            raise jsbachExceptions(msg)

        for i in range(len(self.firstParams)):
            Scope[funcParams[i]] = self.firstParams[i]
        self.visit(Func.context)
        self.SymbolTable.pop()

    # ------------------- FUNCTION RULE ------------------ #

    def visitProcedure(self, ctx):
        self.visit(ctx.parameters())
        self.visit(ctx.statements())

    # ------------------- PARAMETERS RULE ------------------ #

    def visitParameters(self, ctx):
        params = []
        for i in ctx.getChildren():
            id = self.visit(i)
            Scope = self.SymbolTable[self.actualScope]
            Scope[id] = 0
            params += [i.getText()]
        return params

    # ------------------- PARAMSTRING RULE ------------------ #

    def visitParamstring(self, ctx):
        return ctx.STRING().getText()

    # ------------------- WRITEPARAMS RULE ------------------ #

    def visitWriteparams(self, ctx):
        chd = list(ctx.getChildren())
        for i in chd:
            val = self.visit(i)
            print(val)

    # ------------------- STATEMENT RULE ------------------ #

    def visitAssignStmt(self, ctx):
        (id, offset) = self.visit(ctx.left_expr())
        value = self.visit(ctx.expr())
        if id == "_ksg_":
            self.key = value
        elif id == "_tmp_":
            self.tempo = value
        elif id == "_ctm_":
            self.compas = value
        else:
            Scope = self.SymbolTable[self.actualScope]
            if offset != -1:
                array = Scope[id]
                if offset < 1 or offset > len(array):
                    msg = "Out of bounds write access in array: " + id + "[" + str(offset) + "]"
                    raise jsbachExceptions(msg)

                array[offset-1] = value
                Scope[id] = array
            else:
                Scope[id] = value
            self.SymbolTable[self.actualScope] = Scope

    def visitIfStmt(self, ctx):
        chd = list(ctx.getChildren())
        expr = self.visit(ctx.expr())
        if expr:
            self.visit(ctx.statements(0))
        else:
            if len(chd) > 5:
                self.visit(ctx.statements(1))

    def visitWhileStmt(self, ctx):
        expr = self.visit(ctx.expr())
        while expr:
            self.visit(ctx.statements())
            expr = self.visit(ctx.expr())

    def visitParamexp(self, ctx):
        params = []
        exprs = list(ctx.getChildren())
        for oneExpr in exprs:
            e = self.visit(oneExpr)
            params.append(e)
        return params

    def visitProcCall(self, ctx):
        chd = list(ctx.getChildren())
        passedParams = []
        if len(chd) == 2:
            passedParams = self.visit(ctx.paramexp())
        procid = self.visit(ctx.procident())
        Func = self.Procedures[procid]

        Scope = {}
        self.actualScope += 1
        self.SymbolTable.append(Scope)
        funcParams = self.visit(Func.params)

        if len(passedParams) != len(funcParams):
            msg = "Passed params in calling function don't match with params in " + Func.name
            raise jsbachExceptions(msg)

        if len(chd) == 2:
            for i in range(len(passedParams)):
                Scope[funcParams[i]] = passedParams[i]

        self.visit(Func.context)
        self.SymbolTable.pop()
        self.actualScope -= 1

    def visitReadStmt(self, ctx):
        id = ctx.VARID().getText()
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = input()

    def visitWriteStmt(self, ctx):
        self.visit(ctx.writeparams())

    def decodeNote(self, note):
        accidental = ""
        tempo = ""
        if note >= 52*8:
            note -= 52*8
            tempo = "16"
        elif note >= 52*6:
            note -= 52*6
            tempo = "8"
        elif note >= 52*4:
            note -= 52*4
            tempo = "4"
        elif note >= 52*2:
            note -= 52*2
            tempo = "2"
        elif note >= 52:
            note -= 52
            tempo = "1"

        if isinstance(note, float):
            acc = note % 1
            # Tenim un bemol en la nota
            if acc == 0.25:
                note -= 0.25
                accidental = 'es'
            # Tenim un sostingut en la nota
            elif acc == 0.75:
                note -= 0.75
                accidental = 'is'
            else:
                msg = "Non playable note with value " + note
                raise jsbachExceptions(msg)
        
        val = (int(note)-2) % 7
        valuesToNotes = {0: "c", 1: "d", 2: "e", 3: "f", 4: "g", 5: "a", 6: "b"}
        toneToValue = {1: ",,", 2: ",", 3: "", 4: "'", 5: "''", 6: "'''", 7: "''''", 8: "'''''"}
        snote = valuesToNotes[val]
        if note == 0:
            snote = "a" + accidental + ",,,"
        elif note == 1:
            snote = "b" + accidental + ",,,"
        else:
            diff = abs(note-val-2)
            tone = (diff//7)+1
            snote += accidental
            snote += toneToValue[tone]
        snote += tempo
        snote += " "
        return snote

    def playOneNote(self, note):
        snote = self.decodeNote(note)
        self.notesString += snote
        if len(self.notesString) % 7 == 0:
            self.notesString += "\n"
            self.notesString += "         "

    def playChord(self, notes):
        self.notesString += '<'
        for n in notes:
            snote = self.decodeNote(n)
            self.notesString += snote
        self.notesString += '>4 \n'

    def visitPlayStmt(self, ctx):
        notes = self.visit(ctx.expr())
        if isinstance(notes, int) or isinstance(notes, float):
            self.playOneNote(notes)
        else:
            for n in notes:
                if isinstance(n, list):
                    self.playChord(n)
                else:
                    self.playOneNote(n)

    def visitAddToListStmt(self, ctx):
        id = ctx.varident().VARID().getText()
        array = self.visit(ctx.varident())
        elem = self.visit(ctx.expr())
        array += [elem]
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = array
        self.SymbolTable[self.actualScope] = Scope

    def visitCutFromListStmt(self, ctx):
        id = ctx.varident().VARID().getText()
        array = self.visit(ctx.varident())
        offset = self.visit(ctx.expr())
        if offset-1 < 0 or offset-1 >= len(array):
            msg = "Out of bounds delete index in array: " + id + "[" + str(offset) + "]"
            raise jsbachExceptions(msg)
        del array[offset-1]
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = array
        self.SymbolTable[self.actualScope] = Scope

    # ------------------- EXPR RULE ------------------ #

    def visitParenthesis(self, ctx):
        return self.visit(ctx.expr())

    def visitUnary(self, ctx):
        op, expr = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val = self.visit(expr)
        if op == "PLUS":
            return val
        elif op == "MINUS":
            return -val
        else:
            return not val

    def visitArrayReadAccess(self, ctx):
        array = self.visit(ctx.varident())
        offset = self.visit(ctx.expr())
        if not isinstance(offset, int):
            raise jsbachExceptions("Non integer index (" + str(offset) +") in array access " + array)
        if offset < 1 or offset > len(array):
            arrayId = ctx.varident().VARID().getText();
            msg = "Out of bounds read access in array: " + arrayId + "[" + str(offset) + "]"
            raise jsbachExceptions(msg)
        return array[offset-1]

    def visitArithmetic(self, ctx):
        expr1, op, expr2 = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        val2 = self.visit(expr2)
        if op == "MUL":
            return val1 * val2
        elif op == "DIV":
            if val2 == 0:
                raise jsbachExceptions("Attempt to divide by zero")
            return val1 // val2
        elif op == "MOD":
            if val2 == 0:
                raise jsbachExceptions("Attempt to divide by zero")
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
            return val1 == val2
        elif op == "NEQ":
            return val1 != val2
        elif op == "LET":
            return val1 < val2
        elif op == "LEQ":
            return val1 <= val2
        elif op == "GET":
            return val1 > val2
        else:
            return val1 >= val2

    def visitListsSize(self, ctx):
        id = self.visit(ctx.varident())
        return len(id)

    def visitBoolean(self, ctx):
        expr1, op, expr2 = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        if op == "AND":
            if not val1:
                return False
            else:
                val2 = self.visit(expr2)
                return val1 and val2
        else:
            if val1:
                return True
            else:
                val2 = self.visit(expr2)
                return val1 or val2

    def visitRandomNumber(self, ctx):
        ini = self.visit(ctx.expr(0))
        end = self.visit(ctx.expr(1))
        if not isinstance(ini, int) or not isinstance(end, int):
            msg = "Non integer domain for random generator: [" + str(ini) + ", " + str(end) + "]"
            raise jsbachExceptions(msg)
        if ini > end:
            msg = "Incorrect domain in random generator: [" + str(ini) + ", " + str(end) + "]"
            raise jsbachExceptions(msg)
        rand = randint(ini, end)
        return rand

    def visitExprArray(self, ctx):
        return self.visit(ctx.arraytype())

    def visitExprNotes(self, ctx):
        return self.visit(ctx.notes())

    def visitValue(self, ctx):
        chd = list(ctx.getChildren())
        if chd[0].getText() == 'true':
            return True
        elif chd[0].getText() == 'false':
            return False
        elif '.' in chd[0].getText():
            return float(chd[0].getText())
        else:
            return int(chd[0].getText())

    def visitExprIdent(self, ctx):
        return self.visit(ctx.varident())

    # ------------------- LEFT_EXPR RULE ------------------#

    def visitLeft_expr(self, ctx):
        chd = list(ctx.getChildren())
        id = chd[0].getText()
        offset = -1
        if len(chd) > 1:
            offset = self.visit(ctx.expr())
        return (id, offset)

    # ------------------- ARRAYTYPE RULE ------------------#

    def visitArraytype(self, ctx):
        chd = list(ctx.getChildren())
        l = []
        index = 0
        for i in chd:
            c = i.getText()
            if index != 0 and index != len(chd)-1:
                val = self.visit(i)
                l.append(val)
            index += 1
        return l

    # ------------------- NOTES RULE ------------------ #

    def codeNote(self, note):
        notesToValues = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}
        accidentalToValue = {"#": 0.75, "b": 0.25}
        val = note[0]
        prod = 1
        offset = 0

        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 3*7+2
        elif len(note) == 2:
            if note[1] != "#" and note[1] != "b":
                offset = (int(note[1])-1)*7+2
            else:
                acc = note[1]
                offset = 3*7+2 + accidentalToValue[acc]

        elif len(note) == 3:
            if note[1] == ',':
                offset = 3*7+2 + int(note[2])*52
            else:
                acc = note[2]
                offset = (int(note[1])-1)*7+2 + accidentalToValue[acc]
        elif len(note) == 4:
            tmp = note[3]
            if note[1] != "#" and note[1] != "b":
                offset = (int(note[1])-1)*7+2 + int(tmp)*52
            else:
                offset = 3*7+2 + int(tmp)*52
        else:
            acc = note[2]
            tmp = note[4]
            offset = (int(note[1])-1)*7+2 + accidentalToValue[acc] + int(tmp)*52
        return notesToValues[val]+offset

    def visitNotes(self, ctx):
        chd = list(ctx.getChildren())
        note = ctx.NOTES().getText()
        return self.codeNote(note)

    # ------------------- VARIDENT RULE ------------------ #

    def visitVarident(self, ctx):
        id = ctx.VARID().getText()
        Scope = self.SymbolTable[self.actualScope]
        if id not in Scope:
            Scope[id] = 0
        self.SymbolTable[self.actualScope] = Scope
        if isinstance(Scope[id], list):
            return Scope[id]
        else:
            return int(Scope[id])

    # ------------------- PROCIDENT RULE ------------------#

    def visitProcident(self, ctx):
        procid = ctx.PROCID().getText()
        if procid not in self.Procedures:
            msg = "Call to non existing function named "
            msg += procid
            raise jsbachExceptions(msg)
        return procid

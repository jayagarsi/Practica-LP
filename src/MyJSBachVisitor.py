import sys
from antlr4 import *
from jsbachVisitor import jsbachVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from antlr4.error.ErrorListener import ErrorListener


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

    def getNotesString(self):
        return self.notesString

    def getNotesTempo(self):
        return self.tempo
    
    def getKeySignature(self):
        return self.key

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
            msg = "Passed parameters don't match with parameters in "
            msg += Func.name
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
        id = ctx.VARID().getText()
        exp = self.visit(ctx.expr())
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = exp
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
        passedParams = self.visit(ctx.paramexp())
        procid = self.visit(ctx.procident())
        Func = self.Procedures[procid]

        Scope = {}
        self.actualScope += 1
        self.SymbolTable.append(Scope)
        funcParams = self.visit(Func.params)

        if len(passedParams) != len(funcParams):
            msg = "Passed params in calling function don't match with params in "
            msg += Func.name
            raise jsbachExceptions(msg)

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
        val = note % 7
        valuesToNotes = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g"}
        snote = valuesToNotes[val]

        # Tenim un bemol en la nota
        if note >= 59*2:
            note -= 59*2
            snote += 'es'

        # Tenim un sostingut en la nota
        elif note >= 59:
            note -= 59
            snote += 'is'

        if note > 29:
            if note < 37:
                snote += "'"
            elif note < 44:
                snote += "''"
            elif note < 51:
                snote += "'''"
            elif note < 58:
                snote += "''''"
            else:
                snote += "'''''"
        else:
            if note < 2:
                snote += ",,,,"
            elif note < 9:
                snote += ",,,"
            elif note < 16:
                snote += ",,"
            elif note < 23:
                snote += ","
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
        for note in notes:
            snote = self.decodeNote(note)
            snote = self.decodeNote(note)
            self.notesString += snote
        self.notesString += '> '

    def visitPlayStmt(self, ctx):
        notes = self.visit(ctx.expr())
        if isinstance(notes, int):
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
            msg = "Out of bounds acces in array " + id
            raise jsbachExceptions(msg)
        del array[offset-1]
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = array
        self.SymbolTable[self.actualScope] = Scope

    def visitSetTempo(self, ctx):
        value = ctx.INTVAL().getText()
        self.tempo = value

    def visitSetKeySignature(self, ctx):
        keysig = ctx.KEYSIGS().getText()
        self.key = keysig

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
            raise jsbachExceptions("Non integer index in array access")
        if offset-1 < 0 or offset-1 > len(array):
            arrayId = ctx.varident().VARID().getText();
            msg = "Out of bounds access in array"
            msg += arrayId
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
        val2 = self.visit(expr2)

        if op == "AND":
            return val1 and val2
        else:
            return val1 or val2

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
        else:
            return int(chd[0].getText())

    def visitExprIdent(self, ctx):
        return self.visit(ctx.varident())

    # ------------------- ARRAYTYPE RULE ------------------#

    def visitArraytype(self, ctx):
        chd = list(ctx.getChildren())
        l = []
        for i in chd:
            c = i.getText()
            if c != '{' and c != '}':
                val = self.visit(i)
                l.append(val)
        return l

    # ------------------- NOTES RULE ------------------ #

    def codeNote(self, note):
        notesToValues = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        val = note[0]
        
        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 4*7
        elif len(note) == 2:
            if note[1] == '#':
                offset = 4*7 + 59
            elif note[1] == 'b':
                offset = 4*7 + 59*2
            else:
                offset = int(note[1])*7
        else:
            
            offset = int(note[1])*7
            if note[2] == '#':
                    offset += 59
            elif note[2] == 'b':
                offset += 59*2
        return notesToValues[val]+offset

    def visitNotes(self, ctx):
        chd = list(ctx.getChildren())
        if len(chd) == 1:
            note = ctx.NOTES(0).getText()
            return self.codeNote(note)

        else:
            chord = []
            for i in chd:
                note = i.getText()
                if note != '<' and note != '>':
                    n = self.codeNote(note)
                    chord.append(n)
            return chord



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
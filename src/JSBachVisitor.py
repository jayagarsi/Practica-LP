import sys
from antlr4 import *
from jsbachVisitor import jsbachVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
from antlr4.error.ErrorListener import ErrorListener


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("Error: there are some syntactical or lexical errors")
        sys.exit()


class jsbachExceptions(Exception):
    def __init__(self, message):
        self.message = "Error: " + message


class jsbachFunctionInfo():
    def __init__(self, name, params, context, index):
        self.name = name
        self.params = params
        self.context = context
        self.tableindex = index


class TreeVisitor(jsbachVisitor):
    def __init__(self, firstFunctionName="", firstFunctionParams=[]):
        self.Procedures = {}
        self.SymbolTable = []
        self.notesString = ""
        self.actualScope = 0
        self.lastScope = 0
        self.firstFunction = firstFunctionName
        self.firstParams = firstFunctionParams

    def getNotesString(self):
        return self.notesString

    # ------------------- PROCEDURES RULE ------------------ #

    def visitProcedures(self, ctx):
#        Func = jsbachFunctionInfo("Main", [], ctx.main().statements(), self.lastScope)
        chd = list(ctx.getChildren())
        for proc in chd:
            funcid = proc.FUNCID().getText()
            if funcid in self.Procedures:
                msg = "Already existin function with name "
                raise jsbachExceptions(msg, funcid)
            Scope = {}
            self.SymbolTable.append(Scope)
            params = self.visit(proc.parameters())
            Func = jsbachFunctionInfo(funcid, params, proc.statements(), self.lastScope)
            self.lastScope += 1
            self.Procedures[funcid] = Func
        
        if self.firstFunction != "":
            if self.firstFunction not in self.Procedures:
                if "Main" not in self.Procedures:
                    msg = "Trying to execute a non existing procedure named " 
                    msg.append(self.firstFunction)
                    msg.append(" in a program without Main")
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
        
        self.actualScope = Func.tableindex
        Scope = self.SymbolTable[self.actualScope]

        if len(Func.params) != len(self.firstParams):
            raise jsbachExceptions("Passed params in Main don't match with params in Tremenda")

        for i in range(len(self.firstParams)):
            Scope[Func.params[i]] = self.firstParams[i]
        self.visit(Func.context)

    # ------------------- FUNCTION RULE ------------------ #

    def visitFunction(self, ctx):
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
        funcid = self.visit(ctx.funcident())
        Func = self.Procedures[funcid]
        funcParams = Func.params

        if len(passedParams) != len(funcParams):
            raise jsbachExceptions("Passed params in Main don't match with params in Tremenda")

        previousIndex = self.actualScope
        self.actualScope = Func.tableindex
        Scope = self.SymbolTable[self.actualScope]
        for i in range(len(passedParams)):
            Scope[funcParams[i]] = passedParams[i]
        self.visit(Func.context)
        self.actualScope = previousIndex

    def visitReadStmt(self, ctx):
        id = ctx.VARID().getText()
        Scope = self.SymbolTable[self.actualScope]
        Scope[id] = input()

    def visitWriteStmt(self, ctx):
        self.visit(ctx.writeparams())

    def writeOneNote(self, note):
            val = note % 7
            valuesToNotes = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g"}
            snote = valuesToNotes[val]

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
            self.notesString += snote
            if len(self.notesString) % 7 == 0:
                self.notesString += "\n"
                self.notesString += "         "

    def visitPlayStmt(self, ctx):
        notes = self.visit(ctx.expr())
        if isinstance(notes, int):
            self.writeOneNote(notes)
        else:
            for n in notes:
                self.writeOneNote(n)

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
        else:
            return -val

    def visitArrayReadAccess(self, ctx):
        array = self.visit(ctx.varident())
        offset = self.visit(ctx.expr())
        if not isinstance(offset, int):
            raise jsbachExceptions("Non integer index in array access")
        if offset-1 < 0 or offset-1 > len(array):
            raise jsbachExceptions("Out of bounds access in array")
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

    def visitListsSize(self, ctx):
        id = self.visit(ctx.varident())
        return len(id)

    def visitExprArray(self, ctx):
        return self.visit(ctx.arraytype())

    def visitExprNotes(self, ctx):
        return self.visit(ctx.notes())

    def visitValue(self, ctx):
        return int(ctx.INTVAL().getText())

    def visitExprIdent(self, ctx):
        return self.visit(ctx.varident())

    # ------------------- ARRAYTYPE RULE ------------------#

    def visitArraytype(self, ctx):
        chd = list(ctx.getChildren())
        l = []
        for i in chd:
            c = i.getText()
            if c != '{' and c != ',' and c != '}':
                val = self.visit(i)
                l.append(val)
        return l

    # ------------------- NOTES RULE ------------------ #

    def visitNotes(self, ctx):
        note = ctx.NOTES().getText()
        notesToValues = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        val = note[0]

        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 4*7
        else:
            if note == "A" or note == "B":
                offset = int(note[1])*7
            else:
                offset = (int(note[1])+1)*7
            offset = int(note[1])*7

        return notesToValues[val]+offset

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

    # ------------------- FUNCIDENT RULE ------------------#

    def visitFuncident(self, ctx):
        funcid = ctx.FUNCID().getText()
        if funcid not in self.Procedures:
            raise jsbachExceptions("Call to non existing function")
        return funcid

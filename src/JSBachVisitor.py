from antlr4 import *
from jsbachVisitor import jsbachVisitor
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser

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

    def __init__(self, firstFunctionName="Main", firstFunctionParams=[]):
        self.Procedures = {}
        self.SymbolTable = []
        self.notesString = ""
        self.actualScope = 0
        self.lastScope = 0
        self.firstFunction = firstFunctionName
        self.firstParams = firstFunctionParams

    def getNotesString(self):
        return self.notesString

    def visitProcedures(self, ctx):
        Func = jsbachFunctionInfo("Main", [], ctx.main().statements(), self.lastScope)
        self.lastScope += 1
        self.Procedures["Main"] = Func
        Scope = {}
        self.SymbolTable.append(Scope)
        chd = list(ctx.getChildren())
        i = 0
        for proc in chd:
            if i == 0:
                i += 1
            else:
                funcid = proc.FUNCID().getText()
                Scope = {}
                self.SymbolTable.append(Scope)
                params = self.visit(proc.parameters())
                Func = jsbachFunctionInfo(funcid, params, proc.statements(), self.lastScope)
                self.lastScope += 1
                self.Procedures[funcid] = Func

        Func = self.Procedures["Main"]
        self.visit(Func.context)

    def visitMain(self, ctx):
        self.visit(ctx.statements())

    def visitFunction(self, ctx):
        self.visit(ctx.parameters())
        self.visit(ctx.statements())

    def visitParameters(self, ctx):
        params = []
        for i in ctx.getChildren():
            id = self.visit(i)
            Scope = self.SymbolTable[self.actualScope]
            Scope[id] = 0
            params += [i.getText()]
        return params

    def visitWriteparams(self, ctx):
        chd = list(ctx.getChildren())
        for i in chd:
            val = self.visit(i)
            print(val)

    def visitParamstring(self, ctx):
        return ctx.STRING().getText()

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
        return 0

    def visitPlayStmt(self, ctx):
        return self.visit(ctx.expr())

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
        return int(ctx.INTVAL().getText())

    def visitArray(self, ctx):
        chd = ctx.getChildren()
        l = list(chd)
        return l[0]

    def visitArratype(self, ctx):
        chd = list(ctx.getChildren())
        l = []
        for i in chd:
            if i != ',' and i != '{' and i != '}':
                l += self.visit(i)
        return l

    def visitNotes(self, ctx):
        note = ctx.NOTES().getText()
        snote = ord(str(note[0]))
        snote = snote + 32
        snote = chr(snote)
        notesToValues = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
        if len(note) == 1:      # si no hi ha nombre correspone al 4
            offset = 4*8
            snote = snote + "'4"
        else:
            offset = int(note[1])*8          # les notes van de 8 en 8
            snote = snote + "'" + str(note[1])
        snote = str(snote) + " "
        self.notesString += snote
        val = note[0]
        return notesToValues[val]+offset

    def visitExprIdent(self, ctx):
        return self.visit(ctx.varident())

    def visitVarident(self, ctx):
        id = ctx.VARID().getText()
        Scope = self.SymbolTable[self.actualScope]
        if id not in Scope:
            Scope[id] = 0
        self.SymbolTable[self.actualScope] = Scope
        return int(Scope[id])

    def visitFuncident(self, ctx):
        funcid = ctx.FUNCID().getText()
        return funcid

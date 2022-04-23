import sys
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
            print(self.visit(i))

    def visitMain(self, ctx):
        chd = list(ctx.getChildren())
        self.visit(chd[2])

    def visitAssignStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = self.visit(chd[0])
        exp = self.visit(chd[2])
        SymbolTable[id] = exp

    def visitIfStmt(self, ctx):
        chd = list(ctx.getChildren())
        expr = self.visit(chd[1])
        if expr: self.visit(chd[3])

    def visitWhileStmt(self, ctx):
        chd = list(ctx.getChildren())
        expr = self.visit(chd[1])
        while expr:
            expr = self.visit(chd[1])
            self.visit(chd[3])

    def visitReadStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = self.visit(chd[1])
        SymbolTable[id] = input()
    
    def visitWriteStmt(self, ctx):
        chd = list(ctx.getChildren())
        for i in range(1, len(chd)):
            expr = self.visit(chd[i])
            print(expr)
    
    def visitLeft_expr(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[0])

    def visitParenthesis(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[1])

    def visitUnary(self, ctx):
        op, expr = ctx.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val = self.visit(expr)
        if op == "PLUS": return val
        else: return -val

    def visitArithmetic(self, ctx):
        expr1, op, expr2 = chd.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        val2 = self.visit(expr2)
        if op == "MUL": return val1 * val2
        elif op == "DIV": return val1 / val2
        elif op == "MOD": return val1 % val2
        elif op == "PLUS": return val1 + val2
        else: return val1 - val2
    
    def visitRelational(self, ctx):
        expr1, op, expr2 = chd.getChildren()
        op = jsbachParser.symbolicNames[op.getSymbol().type]
        val1 = self.visit(expr1)
        val2 = self.visit(expr2)
        if op == "EQU":
            if val1 == val2: return 1
            else: return 0
        elif op == "NEQ":
            if val1 != val2: return 1
            else: return 0
        elif op == "LET":
            if val1 < val2: return 1
            else: return 0
        elif op == "LEQ":
            if val1 <= val2: return 1
            else: return 0
        elif op == "GET":
            if val1 > val2: return 1
            else: return 0
        else:
            if val1 >= val2: return 1
            else: return 0

    def visitValue(self, ctx):
        val = ctx.getChildren()
        return int(val.getText())

    def visitExprIdent(self, ctx):
        chd = list(ctx.getChildren())
        return self.visit(chd[0])

    def visitIdent(self, ctx):
        id = ctx.getChildren()
        return chd.getText()

if len(sys.argv) != 2: print("Error: no ha introduit cap fitxer")
else:
    input_stream = FileStream(sys.argv[1])

    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.program()
    
    SymbolTable = {}
    visitor = TreeVisitor(SymbolTable)
    visitor.visit(tree)

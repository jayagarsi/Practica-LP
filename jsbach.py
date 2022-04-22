from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser

class TreeVisitor(jsbachVisitor):
    SymbolTable = {}

    def visitProgram(self, ctx):
        chd = list(ctx.getChildren())
        print(self.visit(chd[0]))

    def visitMain(self, ctx):
        chd = list(ctx.getChildren())
        self.visit(chd[2])

    def visitAssignStmt(self, ctx):
        chd = list(ctx.getChildren())
        id = self.visit(chd[0])
        exp = self.visit(chd[expr])
        SymbolTable[id] = exp


input_stream = FileStream(sys.argv[1])

lexer = jsbachLexer(input_stream)
token_stream = antlr4.CommonTokenStream(lexer)
parser = jsbachParser(token_stream)
tree = parser.program()
print(tree.toStringTree(recog=parser))

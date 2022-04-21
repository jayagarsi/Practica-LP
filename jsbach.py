from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

input_stream = FileStream(sys.argv[1])

lexer = EXprLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = ExprParser(token_stream)
tree = parser.root()
print(tree.toStringTree(recog=parser))
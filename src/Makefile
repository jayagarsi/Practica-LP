grammar = jsbach

antlr: $(grammar).g4
	antlr4 -Dlanguage=Python3 -no-listener -visitor $(grammar).g4

clean: cleanMusic
	rm -f $(grammar).interp $(grammar).tokens \
	   	   $(grammar)Lexer.interp $(grammar)Lexer.py $(grammar)Lexer.tokens \
	       $(grammar)Parser.py $(grammar)Visitor.py
	rm -f -r __pycache__

cleanFiles:
	rm -f *.lily *.pdf *.wav *.midi *.mp3
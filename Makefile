grammar = jsbach
musicFileName = musica

antlr: $(grammar).g4
	antlr4 -Dlanguage=Python3 -no-listener -visitor $(grammar).g4

clean: cleanFiles
	rm -f $(grammar).interp $(grammar).tokens \
	   	   $(grammar)Lexer.interp $(grammar)Lexer.py $(grammar)Lexer.tokens \
	       $(grammar)Parser.py $(grammar)Visitor.py
	rm -r __pycache__

cleanFiles:
	rm $(musicFileName).lily $(musicFileName).pdf \
	   $(musicFileName).wav $(musicFileName).midi $(musicFileName).mp3
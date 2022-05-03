//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
////////      Gramatica per jsbach      //////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////
//////////////////////////////////////////////////

grammar jsbach;

//////////////////////////////////////////////////
/// Parser Rules
//////////////////////////////////////////////////

// A program is a list of functions beginning with a main
program : procedures EOF
        ;

procedures : main (function)*
           ;

main : MAIN BEGINBLOCK statements ENDBLOCK
     ;

function : FUNCID parameters BEGINBLOCK statements ENDBLOCK
         ;

parameters : (varident)*
           ;

paramexp   : (expr)+
           ;

statements : (statement)*
           ;

paramstring : STRING
            ;

writeparams : (paramstring|expr)*
            ;
            
statement  
           : VARID ASSIGN expr                                                               # assignStmt
           | IF expr BEGINBLOCK statements ENDBLOCK (ELSE BEGINBLOCK statements ENDBLOCK)?   # ifStmt
           | WHILE expr BEGINBLOCK statements ENDBLOCK                                       # whileStmt
           | funcident paramexp?                                                             # procCall
           | READ VARID                                                                      # readStmt
           | WRITE writeparams                                                               # writeStmt
           | PLAY expr                                                                       # playStmt
           | varident ADDLIST expr                                                           # addToListStmt
           | CUTLIST varident '[' expr ']'                                                   # cutFromListStmt
           ;

expr : '(' expr ')'                                                 # parenthesis
     | varident '[' expr ']'                                        # arrayReadAccess
     | op=(PLUS|MINUS) expr                                         # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | LEN varident                                                 # lists
     | arraytype                                                    # array
     | INTVAL                                                       # value
     | NOTES                                                        # notes
     | varident                                                     # exprIdent
     ;

arraytype : //'{' ( (NOTES|INTVAL) (',' (NOTES|INTVAL) )* )? '}'
            '{' ( NOTES (',' NOTES )* )? '}'
          | '{' ( INTVAL (',' INTVAL )* )? '}'
          ;

funcident : FUNCID
          ;

varident  : VARID
          ;

/////////////////////////////////////////////////
/// Lexer Rules
//////////////////////////////////////////////////

ASSIGN      : '<-' ;

/*----Aritmetics---*/
PLUS        : '+' ;
MINUS       : '-' ;
MUL         : '*';
DIV         : '/';
MOD         : '%';

/*----Relacionals---*/
EQU         : '==' ;
NEQ         : '!=' ;
LET         : '<';
LEQ         : '<=';
GET         : '>';
GEQ         : '>=';

/*---Entrada/Sortida--*/
WRITE       : '<!>' ;
READ        : '<?>' ;

/*------Condicional-----*/
IF          : 'if' ;
ELSE        : 'else' ;
WHILE       : 'while' ;

/*------Delimitadors-----*/
BEGINBLOCK  : '|:' ;
ENDBLOCK    : ':|' ;

/*------Llistes-----*/
ADDLIST     : '<<' ;
CUTLIST     : '8<' ;
LEN         : '#'  ;

/*-----Notes-----*/
PLAY        : '<:>' ;
NOTES       : ('A'..'G') ('0'..'8')? ;

/*-----Funcions-----*/
MAIN        : 'Main';
FUNCID      : ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')*;             // Function IDs start with a capital letter

/*-----Tipus basics-----*/
VARID       : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
ID          : ('a'..'z' | 'A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
INTVAL      : ('0'..'9')+ ;

STRING    : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;

fragment
ESC_SEQ   : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;

COMMENT     : '~~~' ~('\n' | '\r')* '\r'? '\n' -> skip ;

WS          : (' ' | '\t' | '\r' | '\n')+ -> skip ;
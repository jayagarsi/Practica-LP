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
program : main EOF
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

statement  
           : VARID ASSIGN expr                                                               # assignStmt
           | IF expr BEGINBLOCK statements ENDBLOCK (ELSE BEGINBLOCK statements ENDBLOCK)?   # ifStmt
           | WHILE expr BEGINBLOCK statements ENDBLOCK                                       # whileStmt
           | funcident paramexp?                                                             # procCall
           | READ VARID                                                                      # readStmt
           | WRITE (paramstring|expr)*                                                       # writeStmt
           | PLAY expr                                                                       # playStmt
           | varident ADDLIST expr                                                           # addToListStmt
           | CUTLIST varident '[' expr ']'                                                   # cutFromListStmt
           ;

expr : '(' expr ')'                                                 # parenthesis
     | op=(PLUS|MINUS) expr                                         # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | LEN varident                                                 # lists
     | INTVAL                                                       # value
     | arraytype                                                    # value
     | NOTES                                                        # notes
     | varident                                                     # exprIdent
     ;

arraytype : '{' ( (NOTES|INTVAL) (',' (NOTES|INTVAL) )* )? '}'
          ;

funcident : FUNCID
          ;

varident  : VARID
          ;

/////////////////////////////////////////////////
/// Lexer Rules
//////////////////////////////////////////////////

ASSIGN      : '<-' ;

/*----Relacionals---*/
EQU         : '==' ;
NEQ         : '!=' ;
LET         : '<';
LEQ         : '<=';
GET         : '>';
GEQ         : '>=';

/*----Aritmetics---*/
PLUS        : '+' ;
MINUS       : '-' ;
MUL         : '*';
DIV         : '/';
MOD         : '%';

/*---Entrada/Sortida--*/
WRITE       : '<!>' ;
READ        : '<?>' ;
PLAY        : '<:>' ;

/*------Condicional-----*/
IF          : 'if' ;
ELSE        : 'else' ;
WHILE       : 'while' ;

BEGINBLOCK  : '|:' ;
ENDBLOCK    : ':|' ;

ADDLIST     : '<<' ;
CUTLIST     : '8<' ;
LEN         : '#'  ;

/*-----Notes-----*/
NOTES       : ('A'..'G') ('0'..'8')? 
            ;

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
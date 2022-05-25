grammar jsbach;

//////////////////////////////////////////////////
/// Parser Rules
//////////////////////////////////////////////////

// A program is a list of functions beginning with a main
program : procedures EOF
        ;

procedures : (procedure)+
           ;

procedure : PROCID parameters BEGINBLOCK statements ENDBLOCK
         ;

parameters : (varident)*
           ;

statements : (statement)*
           ;

paramexp   : (expr)+
           ;

paramstring : STRING
            ;

writeparams : (paramstring|expr)*
            ;

statement  : VARID ASSIGN expr                                                               # assignStmt
           | KEYSIGNATURE ASSIGN KEYSIGS                                                     # setKeySignature
           | TEMPO ASSIGN INTVAL                                                             # setTempo
           | COMPASTIME ASSIGN CMPTIME                                                       # setCompasTime
           | IF expr BEGINBLOCK statements ENDBLOCK (ELSE BEGINBLOCK statements ENDBLOCK)?   # ifStmt
           | WHILE expr BEGINBLOCK statements ENDBLOCK                                       # whileStmt
           | procident paramexp?                                                             # procCall
           | READ VARID                                                                      # readStmt
           | WRITE writeparams                                                               # writeStmt
           | PLAY expr                                                                       # playStmt
           | varident ADDLIST expr                                                           # addToListStmt
           | CUTLIST varident '[' expr ']'                                                   # cutFromListStmt
           ;

expr : '(' expr ')'                                                 # parenthesis
     | varident '[' expr ']'                                        # arrayReadAccess
     | op=(NOT|PLUS|MINUS) expr                                     # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | LEN varident                                                 # listsSize
     | expr op=AND expr                                             # boolean
     | expr op=OR  expr                                             # boolean
     | arraytype                                                    # exprArray
     | notes                                                        # exprNotes
     | (INTVAL|FLOATNUM|BOOLVAL)                                    # value
     | varident                                                     # exprIdent
     ;

arraytype : '{' (expr)* '}'
          ;

notes : NOTES
      | '<' (NOTES)+ '>'
      ;

procident : PROCID
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
NEQ         : '/=' ;
LET         : '<';
LEQ         : '<=';
GET         : '>';
GEQ         : '>=';

/*----Logics---*/
NOT         : 'not' ;
AND         : 'and' ;
OR          : 'or'  ;

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
NOTES       : ('A'..'G') ('0'..'8')? ('#'|'b')? (',' ('1'|'2'|'8'|'16'))? ;
KEYSIGNATURE: '_ksg_';
TEMPO       : '_tmp_';
COMPASTIME  : '_ctm_';
KEYSIGS     : ('A'..'G') ('major' | 'minor') ;
CMPTIME     : ('2'..'6') '/' ('2'..'6');

/*-----Funcions-----*/
PROCID      : ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')*;             // Function IDs start with a capital letter

/*-----Tipus basics-----*/
BOOLVAL     : 'true' | 'false' ;
VARID       : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
INTVAL      : ('0'..'9')+ ;
FLOATNUM    : ('0'..'9')+ '.' ('0'..'9')+;

STRING    : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;

fragment
ESC_SEQ   : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;

COMMENT     : '~~~' ~('\n' | '\r')* '~~~' -> skip ;

WS          : (' ' | '\t' | '\r' | '\n')+ -> skip ;

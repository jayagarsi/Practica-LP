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

statement  : left_expr ASSIGN expr                                                           # assignStmt
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
     | expr op=AND expr                                             # boolean
     | expr op=OR  expr                                             # boolean
     | LEN varident                                                 # listsSize
     | RANDOM '['expr  expr']'                                      # randomNumber
     | arraytype                                                    # exprArray
     | notes                                                        # exprNotes
     | (INTVAL|FLOATNUM|BOOLVAL)                                    # value
     | varident                                                     # exprIdent
     ;

left_expr : VARID ('[' expr ']')?
          | KEYSIGNATURE
          | TEMPO
          | COMPASTIME
          ;

arraytype : '{' (expr|arraytype)* '}'
          ;

notes : NOTES
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
NOTES       : ('A'..'G') ('0'..'8')? ('#'|'b')? ( ',' ('1'|'2'|'4'|'6'|'8'))?;
KEYSIGNATURE: '_ksg_';
TEMPO       : '_tmp_';
COMPASTIME  : '_ctm_';
KEYSIGS     : ('A'..'G') ('major' | 'minor') ;
CMPTIME     : ('2'..'6') '/' ('2'..'6');

/*-----Funcions-----*/
RANDOM      : 'random';
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

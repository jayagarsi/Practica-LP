grammar jsbach;

//////////////////////////////////////////////////
/// Parser Rules
//////////////////////////////////////////////////

// A program is a set of procedures followed by and End Of Line
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
     | op=(NICHT|PLUS|MINUS) expr                                   # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | expr op=UND expr                                             # boolean
     | expr op=ODER  expr                                           # boolean
     | LEN varident                                                 # listsSize
     | RANDOM '['expr  expr']'                                      # randomNumber
     | arraytype                                                    # exprArray
     | notes                                                        # exprNotes
     | (INTVAL|FLOATNUM)                                            # value
     | varident                                                     # exprIdent
     ;

left_expr : VARID ('[' expr ']')?
          ;

arraytype : '{' (expr)* '}'
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

/*----Arithmetics---*/
PLUS        : '+' ;
MINUS       : '-' ;
MUL         : '*';
DIV         : '/';
MOD         : '%';

/*----Relationals---*/
EQU         : '==' ;
NEQ         : '/=' ;
LET         : '<';
LEQ         : '<=';
GET         : '>';
GEQ         : '>=';

/*----Logic---*/
NICHT       : 'nicht' ;
UND         : 'und' ;
ODER        : 'oder'  ;

/*---Input/Output--*/
WRITE       : '<!>' ;
READ        : '<?>' ;

/*------Conditional-----*/
IF          : 'if' ;
ELSE        : 'else' ;
WHILE       : 'while' ;

/*------Delimiters-----*/
BEGINBLOCK  : '|:' ;
ENDBLOCK    : ':|' ;

/*------Lists-----*/
ADDLIST     : '<<' ;
CUTLIST     : '8<' ;
LEN         : '#'  ;

/*-----Notes-----*/
PLAY        : '<:>' ;
NOTES       : ('A'..'G') ('0'..'8')? ('#'|'b')? (',' ('1'|'2'|'4'|'6'|'8'))?;
KEYSIGNATURE: '_ksg_';
TEMPO       : '_tmp_';
COMPASTIME  : '_ctm_';
KEYSIGS     : ('A'..'G') ('major' | 'minor') ;
CMPTIME     : ('2'..'6') '/' ('2'..'6');

/*-----Functions-----*/
RANDOM      : 'random';
PROCID      : [A-Z\u0080-\u00FF] [0-9a-zA-Z\u0080-\u00FF_]*;             // Function IDs start with a capital letter

/*-----Basic Types-----*/
VARID       : [a-z\u0080-\u00FF] [0-9a-zA-Z\u0080-\u00FF_]*;            // Variable IDs start with a lower letter
INTVAL      : ('0'..'9')+ ;
FLOATNUM    : ('0'..'9')+ '.' ('0'..'9')+;

STRING    : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;            // A string can be an escape sequence or something
                                                            // differnt than '' and "
fragment
ESC_SEQ   : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;

/*-----Skiping types-----*/
COMMENT     : '~~~' ~('\n' | '\r')* '~~~' -> skip ;

WS          : (' ' | '\t' | '\r' | '\n')+ -> skip ;

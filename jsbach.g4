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

parameters : (ID)*
           ;

paramexp   : (expr)+
           ;

statements : (statement)*
           ;

statement  
           : left_expr ASSIGN expr                                                  # assignStmt
           | IF expr BEGINBLOCK statements (ELSE BEGINBLOCK statements ENDBLOCK)?   # ifStmt
           | WHILE expr BEGINBLOCK statements ENDBLOCK                              # whileStmt
           | FUNCID paramexp?                                                       # procCall
           | READ ident                                                             # readStmt
           | WRITE (expr)+                                                          # writeStmt
           | PLAY  expr                                                             # playStmt
           | ident ADDLIST expr                                                     # addToListStmt
           | CUTLIST ident '[' expr ']'                                             # cutFromListStmt
           ;

left_expr  : ident
           ;

expr : '(' expr ')'                                                 # parenthesis
     | op=(PLUS|MINUS) expr                                         # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | LEN ident                                                    # lists
     | INTVAL                                                       # value
     | ident                                                        # exprIdent
     ;
        
ident : ID
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

/*-----Funcions-----*/
MAIN        : 'Main';
FUNCID      : ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')*;             // Function IDs start with a capital letter

/*-----Tipus basics-----*/
VARID       : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
ID          : ('a'..'z' | 'A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
INTVAL      : ('0'..'9')+ ;

COMMENT     : '~~~' ~('\n' | '\r')* '\r'? '\n' -> skip ;

WS          : (' ' | '\t' | '\r' | '\n')+ -> skip ;
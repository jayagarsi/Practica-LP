//////////////////////////////////////////////////////////////////////
//
//    Asl - Another simple language (grammar)
//
//    Copyright (C) 2017-2022  Universitat Politecnica de Catalunya
//
//    This library is free software; you can redistribute it and/or
//    modify it under the terms of the GNU General Public License
//    as published by the Free Software Foundation; either version 3
//    of the License, or (at your option) any later version.
//
//    This library is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//    Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public
//    License along with this library; if not, write to the Free Software
//    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
//
//    contact: José Miguel Rivero (rivero@cs.upc.edu)
//             Computer Science Department
//             Universitat Politecnica de Catalunya
//             despatx Omega.110 - Campus Nord UPC
//             08034 Barcelona.  SPAIN
//
//////////////////////////////////////////////////////////////////////

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

statement
           : VARID ASSIGN expr                                                               # assignStmt
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
     | op=(PLUS|MINUS) expr                                         # unary
     | expr op=(MUL|DIV|MOD) expr                                   # arithmetic
     | expr op=(PLUS|MINUS) expr                                    # arithmetic
     | expr op=(EQU|NEQ|LET|LEQ|GET|GEQ) expr                       # relational
     | LEN varident                                                 # listsSize
     | arraytype                                                    # exprArray
     | notes                                                        # exprNotes
     | INTVAL                                                       # value
     | varident                                                     # exprIdent
     ;

arraytype : //
            '{' (notes)* '}'
          | '{' (INTVAL)*'}'
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
PROCID      : ('A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')*;             // Function IDs start with a capital letter

/*-----Tipus basics-----*/
VARID       : ('a'..'z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
ID          : ('a'..'z' | 'A'..'Z') ('a'..'z'|'A'..'Z'|'_'|'0'..'9')* ;
INTVAL      : ('0'..'9')+ ;

STRING    : '"' ( ESC_SEQ | ~('\\'|'"') )* '"' ;

fragment
ESC_SEQ   : '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\') ;

COMMENT     : '~~~' ~('\n' | '\r')* '\r'? '\n' -> skip ;

WS          : (' ' | '\t' | '\r' | '\n')+ -> skip ;
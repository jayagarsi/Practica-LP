# Doble Intèrpret pel llenguatge musical JSBach

Aquest repositori mostra la resolució de la Pràctica de LP del curs 2021-2022 Q2, on s'implementa un doble intèrpret pel llenguatge de programació JSBach. En aquesta pàgina només es mencionaran parts tècniques de la implementació i les extensions realitzades, l'especificació bàsica del llenguatge es pot trobar en el directori [Enunciat](https://github.com/jayagarsi/Practica-LP/tree/master/Enunciat). La doble interpretació ve de primer interpretar el llenguatge JSBach i després generar codi en llenguatge [lillypond](https://lilypond.org/). Aquest README està pensat per explicar com s'ha implementat l'intèrpret.

## Execució de l'Interpret

Per cridar l'intèrpret, cal cridar a python de la següent manera:

```bash
python3 jsbach.py fitxer.jsb [nomfuncio] [parametres]
```
On jsbach.py és l'intèrpret del llenguatge, generat amb la comanda ```antlr4 -Dlanguage=Python3 -no-listener -visitor $(grammar).g4``` d'ANTLR. Per aquesta raó, per poder executar l'intèrpret cal tenir instal·lat python i ANTLR (aquest últim no fa falta doncs en el directori lib ja estan tots els fitxers necessaris per executar-lo, només seria necessari si es fes algún canvi en la gramàtica). La comanda té 3 paràmetres (a part de l'intèrpret i python3):

* **Nom del Fitxer**: tot i ser un llenguatge interpretat, l'intèrpret no permet execució interactiva, només llegeix programes de fitxers i cal que aquests tinguin l'extensió jsb.
* **Nomfuncio**: serveix per donar el nom de la primera funció que es vol executar. Si no es posa cap s'executa per defecte el Main (si n'hi ha)
* **Parametres**: parametres de la funcio que es vulgui cridar en cas que es posi el nom de la funció. Si no són correctes sortirà un error

## Classes utilitzades

Abans d'entrar en l'explicació de la gramàtica i dels visitadors de l'arbre cal entendre quines classes he creat per fer l'intèrpret i perquè.

### TreeVisitor

Principal classe on hi han tots els visitadors. Hereda de la classe que ANTLR genera que es diu jsbachVisitor.py, per a poder re-implementar els visitors que calgui. Els que no s'han reimplementat és perquè la implementació donada ja val i per no repetir codi.

### jsbachExceptions

Classe utilitzada per generar les meves pròpies excepcions quan es troba algún error en temps d'execució. Aquesta simplement genera el missatge "ERROR" més el missatge que se li passi per paràmetre des del visitor. Hereda de la classe Exception, i com a tal, al rebre qualsevol error s'abortarà l'execució. Com és un intèrpret aquest comportament ja és l'esperat.

```python
class jsbachExceptions(Exception):
    def __init__(self, message):
        self.message = "ERROR: " + message
```

### jsbachFunctionInfo

### MyErrorListener

La segona classe és la MyErrorListener que simplement s'usa per aturar l'execució quan es troben errors sintàctics o lèxics. Si hi ha errors sintàctics no té sentit seguir amb l'execució del programa doncs l'interpretació fallarà i per tant és més pràctic aturar l'execució.

```python
class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("Error: there are some syntactical or lexical errors")
        sys.exit()
```
Per terminar l'execució al script principal l'únic que cal afegir és la comanda ```parser.addErrorListener(MyErrorListener())``` i d'aquesta manera antlr ja s'encarregarà de cridar a MyErrorListener quan es trobi errors sintàctics o lèxics.

```python
input_stream = FileStream(sys.argv[1])

lexer = jsbachLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)
parser.addErrorListener(MyErrorListener())
```
### CodeAndAudioGenerator

## Gramàtica de JSBach

La gramàtica pel llenguatge segueix la mateixa estructura que la proposada en l'enunciat, a diferència de les extensions fetes de les que parlaré més endavant. Aquesta es divideix bàsicament en 4 blocs diferents: regles pels procediments, regles per les instruccions, regles per les expressions i tokens del llenguatge. Per mirar de reduïr l'extensió dels visitadors de l'arbre de sintaxis abstracte, he fet la gramàtica molt modular, generant noves regles per relegar feina i reduir la quantitat de feina per visitador. La gramàtica es pot consultar [aquí](https://github.com/jayagarsi/Practica-LP/tree/master/src/jsbach.g4).

## Visitadors de l'arbre



## Extensions

En aquest apartat entraré més en detall en totes les extensions que he realitzat per millorar el JSBach ja donat i aconseguir un llenguatge més expressiu.

### Operacions amb booleans

### Nombres i Operacions amb Reals

### Nombres aleatòris

### Sostinguts i Bemols

### Canvi de Tempo de la Negra (base)

### Canvi de Tempo d'una Nota

### Canvi d'Armadura

### Acords

Tal i com permet el llenguatge lilypond, JSBach també permet tocar acords utilitzant la notació següent: ```< NOTE_1, ..., NOTE_N >``` generant un acord amb les notes introduïdes. D'aquesta manera, al executar el [codi de prova de l'extensió 3](https://github.com/jayagarsi/Practica-LP/blob/master/Exemples/prova_extensio_03.jsb), obtindrem la següent partitura:


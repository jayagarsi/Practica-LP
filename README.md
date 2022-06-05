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

Aquesta classe realment no és necessària, però he pensat que una manera fàcil de emmagatzemar la informació dels procediemnts era fent una classe auxiliar que té tres atributs només: el nom de la funció, el context dels paràmetres de la funció i el context dels statements de la funció. Com ja he dit, no hauría fet falta fer una classe però penso que fa el codi més llegible.

```python
class jsbachFunctionInfo():
    def __init__(self, name, params, context):
        self.name = name
        self.params = params
        self.context = context
```

### MyErrorListener

La segona classe és la MyErrorListener que simplement s'usa per aturar l'execució quan es troben errors sintàctics o lèxics. Si hi ha errors sintàctics no té sentit seguir amb l'execució del programa doncs l'interpretació fallarà i per tant és més pràctic aturar l'execució.

```python
class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("ERROR: there are some syntactical or lexical errors")
        sys.exit()
```
Per terminar l'execució al script principal l'únic que cal afegir és la comanda ```parser.addErrorListener(MyErrorListener())``` i d'aquesta manera antlr ja s'encarregarà de cridar a MyErrorListener quan es trobi errors sintàctics o lèxics.

```python
input_stream = FileStream(sys.argv[1])

lexer = jsbachLexer(input_stream)
lexer.addErrorListener(MyErrorListener())
token_stream = CommonTokenStream(lexer)
parser = jsbachParser(token_stream)
parser.addErrorListener(MyErrorListener())
```
### CodeAndAudioGenerator

La última classe auxiliar que he creat és la que genera el codi en lilypond, amb el qual ja es podrà generar la partitura en pdf i la seva interpretació en wav i mp3.

## Gramàtica de JSBach

La gramàtica pel llenguatge segueix la mateixa estructura que la proposada en l'enunciat, a diferència de les extensions fetes de les que parlaré més endavant. Aquesta es divideix bàsicament en 4 blocs diferents: regles pels procediments, regles per les instruccions, regles per les expressions i tokens del llenguatge. Per mirar de reduïr l'extensió dels visitadors de l'arbre de sintaxis abstracte, he fet la gramàtica molt modular, generant noves regles per relegar i reduir la quantitat de feina per visitador. La gramàtica es pot consultar [aquí](https://github.com/jayagarsi/Practica-LP/tree/master/src/jsbach.g4).

## Visitadors de l'arbre

## Errors que s'han tingut en compte



## Extensions

En aquest apartat entraré més en detall en totes les extensions que he realitzat per millorar el JSBach ja donat i aconseguir un llenguatge més expressiu.

### Operacions booleanes

La primera extensió afegida a la pràctica és la possibilitat de tenir operacions booleanes com l'AND, l'OR i el NOT. Com George Boole és molt posterior a Bach, el concepte de booleà no existía però calia representar condicios lògiques igualment, com ```a == 4 and b > 2```. D'aquesta manera, per implementar això, el llenguatge bach incorpora les mateixes operacions però amb els noms en alemany (doncs és com Bach li hauria dit). La notació es pot veure en el següent codi:

```   
~~~ prova_extensio_02.jsb ~~~

if nicht b |:
    <!> "Variable b es falsa"
:|

if a und b |:
    <!> "Les dues variables son certes"
:|

if a oder b |:
    <!> "Alguna de les variables es certa"
:|
```
L'equivalència amb Boole sería la següent:
    
| **Boole** | **JSBach** |
|-----------|------------|
| and       | und        |
| or        | oder       |
| not       | nicht      |

Tal i com ve especificat en el llenguatge, no hi ha valors booleans però 0 és fals i qualsevol altra cosa és cert.

### Nombres i Operacions amb Reals

La següent extensió ha sigut més aviat necessària per poder realitzar sostinguts i bemols, doncs facilita molt la feina. No hi ha molt a dir, la notació és la típica de qualsevol llenguatge, un valor enter seguit d'un punt i un valor fraccionari:

```
~~~ prova_extensio_06.jsb

Main |:
  a <- 3.0
  b <- 5.4
  <!> a+b           ~~~ la sortida es 8.4 ~~~
:|

```

El tractament dels floats no és especial, simplement ara en comptes de tractar tots els valors com enters, s'ha de comprovar si el valor és un float i fer el cast implícit en cas que faci falta. Cal destacar que valors com 3.0 poden ser escrits però es tractaran com a floats igualment (tal i com fa Python).

### Nombres aleatòris

Per acabar amb les extensions menys musicals, parlaré de la generació de nombres aleatoris que dóna JSBach. Per generar un nombre aleatòri simplement s'ha d'escriure ```random [ini end]```, on ini i end són l'interval en que es genera el nombre. Random és una expressió en JSBach, així que ha d'anar acompanyat d'un statement. Un codi d'exemple el podem veure en el següent:

```
~~~ prova_extensio_09.jsb ~~~
RandomAssign a |:
    while i <= 50 |:
        val <- random[3 12]
        a << val
        i <- i+1
    :|
    <!> a                   ~~~ genera una llista amb 50 nombres aleatoris entre 3 i 12
:|
```
Cal destacar que el generador de nombres aleatòris només genera enters no reals, i per tant els intervals també han de ser enters. Per evitar errors doncs, l'intèrpret comprova si els intervals són correctes. Els dos missatges d'error que s'emeten passen quan:
* Un dels dos límits és un valor real (p.e. \[4.2, 3\])
* Els límits se sobreposen (p.e. \[3, 2\])

### Sostinguts i Bemols

Ara, podem començar amb les extensions musicals. La primera implementada és la possibilitat de tocar notes amb accidentals, siguin bemolls o sostinguts. La codificació per aquests m'ha portat bastants problemes, però al final he decidit codificar-ho en la pròpia nota. Aquí és on entren en joc els nombres reals. Abans que res, en la gramàtica les notes amb bemolls les he definit de la següent manera: ```NOTE : ('A'..'G') ('0'..'8')? ('#'|'b')?```. D'aquesta manera, les notes es poden esciure així ```A0# B2b C3```, etc. Com el llenguatge està pensat per músics, he cregut que aquesta era la millor notació. Aquí hi tenim un exemple:

```
~~~ prova_extensio_01.jsb ~~~

Main |:
    <!> "Programa per sostinguts i bemols"
    a <- {C4b A5# G3b}
    <!> a
    <:> a
:|
```

Cal parlar també una mica de la codificació. Com els accidentals estan codificats en la pròpia nota, cal donar un valor nou a cada nota quan tinguem un sostingut o un bemoll. Per evitar complicacions, he seguit la següent notació:
* Si la nota té valor real i la part fraccional val 0.25 --> tenim un bemol
* Si la nota té valor real i la part fraccional val 0.75 --> tenim un sostingut
Aquesta notació és poc intuitiva, sobretot pels músics, però facilita molt la feina per part del compilador. D'aquesta manera al codificar la nota només cal fer el següent:

```python
...
accidentalToValue = {"#": 0.75, "b": 0.25}
...
if note[1] != "#" and note[1] != "b":
    offset = (int(note[1])-1)*7+2
else:
    acc = note[1]
    offset = 3*7+2 + accidentalToValue[acc]
...
```

I alhora de decodificar:

```python
if isinstance(note, float):
    acc = note % 1
    # Tenim un bemol en la nota
    if acc == 0.25:
        note -= 0.25
        accidental = 'es'
    # Tenim un sostingut en la nota
    elif acc == 0.75:
        note -= 0.75
        accidental = 'is'
    else:
        msg = "Non playable note with value " + note
        raise jsbachExceptions(msg)
```

Com es pot veure, si el valor fraccionari no és ni 0.25 ni 0.75, s'envia un error de que aquella nota no es pot tocar. Per aquesta raó cal anar amb molt de compte alhora de tocar notes posant els seus valors numérics. Per veure amb més detall això es pot anar al codi del TreeVisitor.

### Canvi de Tempo de la Negra (base)

### Canvi de Tempo d'una Nota

### Canvi d'Armadura

### Acords

Tal i com permet el llenguatge lilypond, JSBach també permet tocar acords utilitzant la notació següent: ```< NOTE_1, ..., NOTE_N >``` generant un acord amb les notes introduïdes. D'aquesta manera, al executar el [codi de prova de l'extensió 3](https://github.com/jayagarsi/Practica-LP/blob/master/Exemples/prova_extensio_03.jsb), obtindrem la següent partitura:


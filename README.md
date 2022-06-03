# Doble Intèrpret pel llenguatge musical JSBach

Pràctica de LP del curs 2021-2022 Q2 on s'implementa un doble intèrpret pel llenguatge de programació JSBach. La definició del llenguatge es troba en el directori [Enunciat](https://github.com/jayagarsi/Practica-LP/tree/master/Enunciat). La doble interpretació ve de que primer s'interpreta el llenguatge JSBach i després es genera codi en llenguatge [lillypond](https://lilypond.org/). Aquest README està pensat per explicar com s'ha implementat l'intèrpret i entendre millor.

## Gramàtica de JSBach

Abans d'entrar en els visitadors de l'arbre cal entendre la gramàtica i les 

## Classes auxiliars utilitzades

Abans d'entrar en l'explicació del visitador de l'arbre cal entendre quines classes auxiliars he utilitzat per fer l'intèrpret.


La primera classe utilitzada és la jsbachExceptions que simplement l'he creat per generar les meves pròpies excepcions quan es troba algún error en temps d'execució. Aquesta simplement genera el missatge "Error" més el missatge que se li passi per paràmetre des del visitor.

```python
class jsbachExceptions(Exception):
    def __init__(self, message):
        self.message = "Error: " + message
```

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


## Extensions

Aquí explicaré amb més detall totes les extensions que he realitzat per la pràctica

### Operacions amb booleans

### Nombres aleatòris

### Sostinguts i Bemols

### Canvi de Tempo de la Negra (base)

### Canvi de Tempo d'una Nota

### Canvi d'Armadura

### Acords

Tal i com permet el llenguatge lilypond, JSBach també permet tocar acords utilitzant la notació següent: ```< NOTE_1, ..., NOTE_N >``` generant un acord amb les notes introduïdes. D'aquesta manera, al executar el [codi de prova de l'extensió 3](https://github.com/jayagarsi/Practica-LP/blob/master/Exemples/prova_extensio_03.jsb), obtindrem la següent partitura:


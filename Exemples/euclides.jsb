~~~ programa que llegeix dos enters i n'escriu el seu maxim comu divisor ~~~

Main |:
    <!> "Escriu dos nombres"
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
	notes <- {A A5 B3 C4# D F}
	size <- #notes
    while a /= b |:
        if a > b |:
            a <- a - b
            <:> notes[a%size+1]
        :| else |:
            b <- b - a
            <:> notes[b%size+1]
        :|
    :|
    <!> "El seu MCD es" a
:|

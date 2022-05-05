~~~ programa que llegeix dos enters i n'escriu el seu maxim comu divisor ~~~

Main |:
    <!> "Escriu dos nombres"
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
    while a /= b |:
        <:> a
        <:> b
        if a > b |:
            a <- a - b
        :| else |:
            b <- b - a
        :|
        if a > D1 |:
            <:> a
            <:> a-b
            <:> a+b
            <:> b
        :|
    :|
    <!> "El seu MCD es" a
:|
~~~ Algorisme que calcula l'n-essim nombre de Fibonacci ~~~

Main |:
    <!> "Introdueix un nombre"
    <?> a
    if a < 0 |:
        <!> "El nombre ha de ser major a 0"
    :|
    else |: Fibonacci a :|
:|

Fibonacci n |:
    a <- 0
    b <- 1
    if n == 0   |: <!> a :|
    if n == 1   |: <!> b :|
    else |:
        i <- 2
        while i <= n+1 |:
            c <- a+b
            a <- b
            b <- c
            i <- i+1
            if a > 15 and a < 70*2 |: <:> a :|
            if b > 15 and b < 70*2 |: <:> b :|
            if c > 15 and c < 70*2 |: <:> c :|
        :|
        <!> b
    :|
:|
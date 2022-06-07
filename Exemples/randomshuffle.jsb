~~~ Algorisme per desordenar array aleatoriament ~~~

Swap a r h |:
    temp <- a[r]
    a[r] <- a[h]
    a[h] <- temp
:|

Randomize a n |:
    i <- n
    while i > 1 |:
        j <- random[1 i]
        Swap a i j
        <:> j*2
        i <- i-1
    :|
:|

Main |:
    a <- {23 14 52 83 9172 490 210 32 12 74 98 23 4908 123 40 29 91 8 27 3 6}
    <!> "Llista original"
    <!> a
    <!> "Desordenant llista..."
    Randomize a #a
    <!> "Llista ordenada"
    <!> a
:|
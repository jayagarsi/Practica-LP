~~~ Joc de Prova per provar la generacio de nombres aleatoris ~~~


RandomAssign a |:
    while i <= 50 |:
        val <- random[3 12]
        a << val
        i <- i+1
    :|
:|

Main |:
    a <- {}
    i <- 1
    RandomAssign a
    <!> a
    <:> a
:|
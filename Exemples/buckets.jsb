~~~ Programa per resoldre el problema d'omplir un cubell amb x litres ~~~
~~~ tenint 2 cubells que poden ser omplerts fins un maxim i es poden ~~~
~~~ buidar del tot, omplir del tot o omplir en l'altre fins que vessi ~~~

Main |:
    n <- 3
    m <- 5
    d <- 4
    FillBucket n m d
:|

FillBucket n m d |:
    Pour n m d
    Pour m n d
:|

Pour cubellDesti cubellOrigen d |:
    cOrig <- cubellOrigen
    cDest <- 0
    maxQ <- 0
    pas <- 1
    while cOrig /= d and cDest /= d |:
        if cOrig > cubellDesti - cDest |: maxQ <- cubellDesti :|
        else |: maxQ <- cOrig :|

        cDest <- cDest + maxQ
        cOrig <- cOrig - maxQ
        pas <- pas + 1

        if cOrig /= d and cDest /= d |:

            if cOrig = 0 |:
                cOrig <- cubellOrigen
                pas <- pas + 1
            :|
            if cDest = cubellDesti |:
                cDest <- 0
                pas <- pas +1 
            :|
        :|
        <:> cOrig*4
        <:> cDest*4
    :|
    <!> pas
:|

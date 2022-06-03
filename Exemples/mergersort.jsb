~~~ Algorisme d'ordenacio Mergesort amb musica ~~~

Merge a l m r |:

    nl <- m-l+1
    nr <- r-m-1

    lArr <- {}
    rArr <- {}

    il <- 1
    while il <= nl |:
        lArr << a[il+1]
        il <- il+1
    :|

    ir <- 1
    while ir <= nl |:
        rArr << a[ir+1]
        ir <- ir+1
    :|    

    i <- 1
    j <- 1
    k <- l
    while i < nl and j < nr |:
        if lArr[i] <= rArr[k] |:
            a[k] <- lArr[i]
            i <- i+1
        :|
        else |:
            a[k] <- rArr[j]
            j <- j+1
        :|
        k <- k+1
    :|

    while i < nl |:
        a[k] <- lArr[i]
        i <- i+1
        k <- k+1
    :|

    while j < nr |:
        a[k] <- rArr[i]
        j <- j+1
        k <- k+1
    :|

:|

Mergesort a l r |:
    if l < r |:
        m <- (l + r)/2
        Mergesort a l m
        Mergesort a m+1 r

        Merge a l m r
    :|
:|

Main |:
    a <- {53 61 8 7 1 0 32}
    <!> "Array original"
    <!> a
    size <- #a
    <!> "Ordenant array..."
    Mergesort a 1 size
    <!> "Array ordenat"
    <!> a
:|
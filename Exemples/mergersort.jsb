~~~ Algorisme d'ordenacio Mergesort amb musica ~~~

Merge a l m r |:

    leftAux <- {}
    rightAux <- {}
    i <- 1
    while i <= #a |:
        leftAux << a[l+i]
        i <- i+1
    :|

    i <- 1
    while i <= #a |:
        leftAux << a[m+l+i]
        i <- i+1
    :|

    i <- 1
    j <- 1
    k <- l+1

    while i <= #leftAux and j <= #rightAux |:
        if leftAux[i] < rightAux[j] |:
            a[k] <- leftAux[i]
            i <- i+1
        :|

        else |:
            a[k] <- rightAux[j]
            j <- j+1
        :|
        k <- k+1
    :|

    while i <= #leftAux |:
        a[k] <- leftAux[i]
        i <- i+1
        k <- k+1
    :|

    while j <= #rightAux |:
        a[k] <- rightAux[j]
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
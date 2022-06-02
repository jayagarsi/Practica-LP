~~~ Algorisme d'ordenacio Insertion Sort amb musica ~~~

InsertionSort a |:
    i <- 2
    while i <= #a |:
        temp <- a[i]
        j <- i-1
        
        while j > 0 and temp <= a[j] |:
            a[j+1] <- a[j]
            j <- j-1
            <:> j*2
        :|
        a[j+1] <- temp

        i <- i+1
    :|
:|

Main |:
    a <- {12 4 3 1 15 42 33 21 10 2}
    <!> "Llista original"
    <!> a
    <!> "Ordenant llista..."
    InsertionSort a
    <!> "Llista ordenada"
    <!> a
:|
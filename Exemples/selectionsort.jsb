~~~ Algorisme d'ordenacio Selection Sort ~~~

SelectionSort a n |:
    minIndex <- 0
    i <- 1
    while i < n |:
        minIndex <- i
        j <- i+1
        while j <= n |:
            if a[j] < a[minIndex] |:
                minIndex <- j
                <:> minIndex*2
            :|
            j <- j+1
            
        :|
        temp <- a[minIndex]
        a[minIndex] <- a[i]
        a[i] <- temp
        i <- i+1
    :|
:|

Main |:
    a <- {64 234 16 20 91 2 45 123 40 18 64 10 92}
    <!> "Llista original"
    <!> a
    <!> "Ordenant llista..."
    SelectionSort a #a
    <!> "Llista ordenada"
    <!> a
:|
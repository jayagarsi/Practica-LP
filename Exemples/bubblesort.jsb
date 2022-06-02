~~~ Algorisme d'ordenacio Bubble Sort amb musica ~~~

BubbleSort a |:
    i <- 1
    size <- #a
    while i <= size |:
        j <- 1
        while j <= size-i-1 |:
            if a[j] > a[j+1] |:
                aux <- a[j]
                a[j] <- a[j+1]
                a[j+1] <- aux
            :|
            <:> j
            j <- j+1
        :|
        i <- i+1
    :|
:|

Main |:
    a <- {5 1 4 2 8 10 231 345 61 239 10}
    <!> "Llista original"
    <!> a
    <!> "Ordenant llista..."
    BubbleSort a
    <!> "Llista ordenada"
    <!> a
:|

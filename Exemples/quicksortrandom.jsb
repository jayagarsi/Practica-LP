~~~ Algorisme d'ordenacio QuickSort amb pivot random ~~~

Main |:
    a <- {123 124 12 5 3 53 3 168 29 71 03 18 321 018 23}
    <!> "Llista original"
    <!> a
    <!> "Ordenant llista..."
    QuickSort a 1 #a
    <!> "Llista ordenada"
    <!> a
:|

Swap a r h |:
    temp <- a[r]
    a[r] <- a[h]
    a[h] <- temp
:|

QuickSort a l h |:
    if l < h |:
        r <- random[l h]
        <:> r
        Swap a l r
        pivot <- l
        i <- l+1
        j <- l+1
        while j <= hi+1 |:
            if a[j] <= a[pivot] |:
                Swap a i j
                i <- i+1
            :|
            j <- j+1
        :|
        Swap a pivot i-1
        pivot <- i-1
        QuickSort a l pivot-1
        QuickSort a pivot+1 h
    :|
:|
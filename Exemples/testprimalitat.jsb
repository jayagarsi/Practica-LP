~~~ Algorisme per saber si un nombre es primer ~~~
~~~    basat en el Petit Teorema de Fermat     ~~~

PlaySomeNote a |:
    ~~~ per tocar algunes notes aleatories amb accidentals ~~~
    dec <- 0
    randdec <- random[1 20]
    if randdec = 1 |:
        dec <- 0.25
    :|
    if randdec = 2 |:
        dec <- 0.75
    :|
    <:> a % 30 + 10 + dec              ~~~ asseguro que sigui una nota tocable ~~~
:|

IsPrime n k |:
    notes <- {A B C D}
    if n = 1 oder n = 4 |:
        <!> "El nombre no es primer"
    :|
    
    if n = 2 oder n = 3 |:
        <!> "El nombre es primer"
    :|

    if n > 4 |:
        i <- 0
        noEsPrimer <- 0

        while i < k |:
            a <- random[2 n-2]
            i <- i+1
            
            ~~~ Calcul de a^(n-1) % n ~~~
            res <- 1
            exp <- n-1
            p <- n
            a <- a % n
            while exp > 0 |:
                if exp%2 |:
                    res <- (res*a)%p
                    exp <- exp-1
                :|
                else |:
                    a <- (a*a)%p
                    exp <- exp/2
                    PlaySomeNote a
                :|
            :|
            res <- res%n
            ~~~                     ~~~

            if res /= 1 |:
                i <- k+1    ~~~ simulo la sortida de la funcio ~~~
                noEsPrimer <- 1
            :|
        :|
        if noEsPrimer |:
            <!> "El nombre no es primer"
        :|
        else |:
            <!> "El nombre possiblement es primer"
        :|
    :|

:|

Main |:
    <!> "Introdueix un nombre"
    <?> n
    <!> "Introdueix el nombre de vegades a repetir l'experiment"
    <?> k
    IsPrime n k
:|
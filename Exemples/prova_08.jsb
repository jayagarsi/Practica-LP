~~~ Prova de canviar el valor d'un array ~~~

Proc a |:
    <!> a
    <!> "Escriu el valor a canviar del primer element"
    <?> b
    a[1] <- b
:|

Main |:
    a <- {1 2 3 4}
    Proc a
    <!> a
:|
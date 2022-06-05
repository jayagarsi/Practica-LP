~~~ Programa per testejar funcions logiques ~~~

Main |:
    <!> "Introdueix 2 nombres per vars a i b"
    <?> a
    <?> b
    if a |:
        <!> "Variable a es certa"
    :|

    if nicht b |:
        <!> "Variable b es falsa"
    :|

    if a und b |:
        <!> "Les dues variables son certes"
    :|

    if a oder b |:
        <!> "Alguna de les variables es certa"
    :|
:|
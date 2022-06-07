~~~ Principi de la Sonata No.14 Beethoven ~~~

Main |:
  Sonata
:|

PlayOneProgression a lim |:
  i <- 0
  while i < lim |:
    <:> a
    i <- i+1
  :|
:|

Sonata |:
  _tmp_ <- 80
  _ksg_ <- Emajor
  progressio <- {{C1,6 C2 G3} C4,6 E4b,6 G3,6 C4,6 E4b,6 G3,6 C4,6 E4b,6 G3,6 C4,6 E4b,6}
  PlayOneProgression progressio 1

  progressio <- {{B0 B1,6 G3} C4,6 E4b,6 G3,6 C4,6 E4b,6 G3,6 C4,6 E4b,6 G3,6 C4,6 E4b,6}
  PlayOneProgression progressio 1

  progressio <- {A3b,6 C4,6 E4b,6}
  PlayOneProgression progressio 2
  
  progressio <- {A3b,6 D4,6 F4,6}
  PlayOneProgression progressio 2

  progressio <- {G3,6 B3#,6 F4,6 G3,6 C4,6 E4b,6}
  PlayOneProgression progressio 1

  progressio <- {G3,6 C4,6 D4,6 F3,6 B3#,6 D4,6 B3,4 {C4,2 C3 C5}}
  PlayOneProgression progressio 1
:|

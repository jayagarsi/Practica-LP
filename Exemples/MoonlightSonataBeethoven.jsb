~~~ Sonata No.14 Beethoven ~~~

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
  _tmp_ = 160
  progressio <- {G3 C4 F4b}
  PlayOneProgression progressio 8
  progressio <- {A4 C4# F4b}
  PlayOneProgression progressio 2
  progressio <- {A4 D4 G4}
:|

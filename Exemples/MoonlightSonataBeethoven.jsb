~~~ Sonata No.14 Beethoven ~~~

Main |:
  ~~~<:> {A0 B0 C1 D1 E1 F1 G1 A1 B1 C2 D2 E2 F2 G2 A2 B2}~~~
  ~~~<:> {C3 D3 E3 F3 G3 A3 B3 C4 D4 E4 F4 G4 A4 B4}~~~
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
  _tmp_ <- 120
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

  progressio <- {G3,6 C4,6 D4,6 F3,6 B3#,6 D4,6}
  PlayOneProgression progressio 1
:|

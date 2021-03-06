import random

time = [0, 8, 4, 4, 2, 2, 1]
time = [4, 4, 4, 4, 4, 4, 4]


def hanoi(n, src, dst, aux):
    if n > 0:
        hanoi(n-1, src, aux, dst)
        x = src[-1]
        del(src[-1])
        dst.append(x)
        print(x+"'"+str(time[n]))
        hanoi(n-1, aux, dst, src)


def main():
    src = ["c", "d", "e", "f", "g"]
    # random.shuffle(src)
    dst = []
    aux = []
    hanoi(len(src), src, dst, aux)


print("""
\\version "2.22.1"
\\score {
\\absolute {
\\tempo 4 = 180
\key c \major
""")
main()
print("""
c'1
}
\\layout { }
\\midi { }
}
""")

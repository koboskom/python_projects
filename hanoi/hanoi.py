def hanoi(n, A, B, C):
   if n>0:
        hanoi(n-1, A, C, B)
        C.append(A.pop())
        print("a", A,"b", B,"c", C)
        hanoi(n-1, B, A, C)
krazki = int(input("liczba krazkow: "))
a = []
b = []
c = []

for i in range(krazki):
    a.append(krazki-i)
print("a", a,"b", b,"c", c)
hanoi(krazki,a,b,c)
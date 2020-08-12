def hanoi(n, A, B, C):

    if n % 2 == 0:
        B = C
        C = A
        A = B
    for i in range(1, pow(2,n)):
        if i % 3 == 1:
            legal(A,C)
        if i % 3 == 2:
            legal(A, B)
        if i % 3 == 0:
            legal(B,C)
        print("a", A,"b", B,"c", C)

def legal(A,B):
    if not len(A):
        A.append(B.pop())
    elif not len(B):
        B.append(A.pop())
    elif int(A[-1]) > int(B[-1]):
        A.append(B.pop())
    else:
        B.append(A.pop())




krazki = int(input("liczba krazkow: "))
a = []
b = []
c = []
for i in range(krazki):
    a.append(krazki-i)
print("a", a,"b", b,"c", c)
hanoi(krazki, a, b, c)
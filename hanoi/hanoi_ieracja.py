import time
start_time = time.time()
def hanoi(n, A, B, C): #nparzyste
    i=0

    while (len(A) !=0 or len(C) != 0 ):
        i+=1

        if i % 3 == 1:
            if len(A) == 0: #BA
                A.append(B.pop())
            elif len(B) == 0:
                B.append(A.pop())
            elif A[len(A)-1] < B[len(B)-1]:
                B.append(A.pop())
            else:
                A.append((B.pop()))

        if i % 3 == 2: #CA
            if len(A) == 0:
                A.append(C.pop())
            elif len(C) == 0:
                C.append(A.pop())
            elif A[len(A) - 1] < C[len(C) - 1]:
                C.append(A.pop())
            else:
                A.append((C.pop()))

        if i % 3 == 0: #BC
            if len(B) == 0:
                B.append(C.pop())
            elif len(C) == 0:
                C.append(B.pop())
            elif B[len(B) - 1] < C[len(C) - 1]:
                C.append(B.pop())
            else:
                B.append((C.pop()))
        #print(i,"a", A,"b", B,"c", C)


def hanoi2(n, A, C, B):  # parzyste
    i = 0

    while (len(A) != 0 or len(C) != 0 and i<pow(2,n)-1):
        i += 1

        if i % 3 == 1:
            if len(A) == 0:  # BA
                A.append(B.pop())
            elif len(B) == 0:
                B.append(A.pop())
            elif A[len(A) - 1] < B[len(B) - 1]:
                B.append(A.pop())
            else:
                A.append((B.pop()))

        if i % 3 == 2:  # CA
            if len(A) == 0:
                A.append(C.pop())
            elif len(C) == 0:
                C.append(A.pop())
            elif A[len(A) - 1] < C[len(C) - 1]:
                C.append(A.pop())
            else:
                A.append((C.pop()))

        if i % 3 == 0:  # BC
            if len(B) == 0:
                B.append(C.pop())
            elif len(C) == 0:
                C.append(B.pop())
            elif B[len(B) - 1] < C[len(C) - 1]:
                C.append(B.pop())
            else:
                B.append((C.pop()))
        #print(i, "a", A, "b", C, "c", B)

krazki = int(input("liczba krazkow: "))
a = []
b = []
c = []
for i in range(krazki):
    a.append(krazki-i)
print("a", a,"b", b,"c", c)
if krazki%2==0:
    hanoi2(krazki, a, b, c)
else:
    hanoi(krazki, a, b, c)

elapsed_time = time.time() - start_time
print (elapsed_time)
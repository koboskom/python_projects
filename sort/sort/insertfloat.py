__author__ = 'Administrator'
import random
import time
l = []
n = 1000
z = 10

czas = []

for k in range(z):
    start_time = time.time()


    def insertionsort(l):
        l = []
        for z in range(n):
            i = random.randint(1,1000)
            l.append(float(i))

        for i in range(1, len(l)):
            x = l[i]
            j = i
            while j > 0 and l[j-1] > x:
                l[j] = l[j-1]
                j = j-1

            l[j] = x

    insertionsort(l)
    czas.append(time.time() - start_time)
def czasuwa():
    print("insertionsort float")
    print(czas)
    suma = 0
    for j in range(z):

        suma = suma+czas[j]

    srednia = suma/len(czas)
    print("suma ", suma)
    print("srednia ", srednia)
    print("max time ", max(czas))
    print("min time ", min(czas))
    print("__________________")
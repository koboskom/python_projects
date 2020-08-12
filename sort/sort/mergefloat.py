__author__ = 'Administrator'
import random
import time
x = []
n = 1000
z = 10
czas = []

for k in range(z):
    start_time = time.time()
    for z in range(n):
        i = random.randint(1, 1000)
        x.append(float(i))

    def msort(x):
        if len(x) < 2:
            return x
        result = []
        mid = int(len(x) / 2)
        y = msort(x[:mid])
        z = msort(x[mid:])
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        return result

    msort(x)
    czas.append(time.time() - start_time)
def czasuwa():
    print("mergesort float")
    print(czas)
    suma = 0
    for j in czas:

        suma = suma + j

    srednia = suma/(len(czas))
    print("suma ", suma)
    print("srednia ", srednia)
    print("max time ", max(czas))
    print("min time ", min(czas))
    print("-----------")
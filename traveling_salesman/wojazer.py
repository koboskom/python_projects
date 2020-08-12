#najblizszy sasiad
f = open("TSP.txt","r")
txt = f.read()
txt2 = txt.replace("\t", " ").replace('\n', "").split(" ")
k = list(txt2)
x = []
y = []

for i in range(1,len(k)):
    if i%2 == 0:
        y.append(float(k[i]))
    else:
        x.append(float(k[i]))

macierz = []
odleglosc = []
for j in range(100):
    odleglosc = []
    for i in range(100):
        odleglosc.append(float(pow(((pow((float(x[j]) - float(x[i])), 2) + pow((float(y[j]) - float(y[i])), 2))), (1 / 2))))
    macierz.append(odleglosc)
for i in macierz:
    print(i)


def sasiedzi(macierz, n, odwiedzone, suma):
    min = 9999.0
    if n not in odwiedzone and len(odwiedzone) < 99:
        for i in macierz[n]:
            if i < min and i != 0.0 and macierz[n].index(i) not in odwiedzone:
                min = i
        k = macierz[n].index(min)
        suma.append(min)
        odwiedzone.append(n)
        sasiedzi(macierz, k, odwiedzone,suma)
vtab =[]
for n in range(99):
    odwiedzone = []
    suma = []
    v = 0

    sasiedzi(macierz, n, odwiedzone, suma)
    for i in suma:
        v += i
    #v += macierz[odwiedzone[-1]][odwiedzone[0]]
    vtab.append(v)
print(sorted(vtab)[0])




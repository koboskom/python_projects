from tsp_solver.greedy import solve_tsp

f = open("TSP.txt","r")
txt = f.read()
txt2 = txt.replace("\t", " ").replace('\n', "").split(" ")
k = list(txt2)
x = []
y = []
suma = 0
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
        odleglosc.append(pow(((pow((float(x[j]) - float(x[i])), 2) + pow((float(y[j]) - float(y[i])), 2))), (1 / 2)))
    macierz.append(odleglosc)



path = solve_tsp( macierz )


print(path)
suma = 0
for i in range(0, len(path)-1):
    suma += macierz[path[i]][path[i+1]]
    print(i," ", suma)
suma += macierz[path[-1]][path[0]]+macierz[path[98]][path[99]]
print(suma)

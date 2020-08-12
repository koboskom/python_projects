
f = open("TSP.txt","r")
txt = f.read()
txt2 = txt.replace("\t", " ").replace('\n', "").split(" ")
k = list(txt2)
x = []
y = []
suma = 0
n = int(input("podaj od ktorego miasta zaczynamy "))
for i in range(1,len(k)):
    if i%2 == 0:
        y.append(k[i])
    else:
        x.append(k[i])
for i in range(n,99):
    suma += pow(((pow((float(x[i])-float(x[i+1])), 2) + pow((float(y[i])-float(y[i+1])), 2))),(1/2))

for i in range(n):
    suma += pow(((pow((float(x[i])-float(x[i+1])), 2) + pow((float(y[i])-float(y[i+1])), 2))),(1/2))

suma += pow(((pow((float(x[99])-float(x[0])), 2) + pow((float(y[99])-float(y[0])), 2))),(1/2))
print(suma)
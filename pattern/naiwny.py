import time
f = open("4000_pattern.txt","r")

start_time = time.time()

txt = f.read()
txt2 = txt.replace("\n", "").replace(" ", "")
n = int(input("podaj wymiar "))
pat = ['A', 'B', 'C']
result = []
o = 0
for i in range(n*n-2*n):
    if pat[0] == txt2[i] and pat[1] == txt2[i+1] and pat[2] == txt2[i+2] and pat[1] == txt2[i+n] and pat[2] == txt2[i+2*n]:
        result.append(i)
        o+=1
elapsed_time = time.time() - start_time
print("tyle ",o)
print(result)
print(elapsed_time)
import time
f = open("4000_pattern.txt","r")

start_time = time.time()

txt = f.read()
txt2 = txt.replace("\n", "").replace(" ", "")
pat = "ABC"
k = int(input("podaj wymiar "))

def rabin(txt2, pat, d, q, k):
    n = len(txt2)
    m = len(pat)
    h = pow(d,m-1)% q
    p = 0
    ts = 0
    o = 0
    result = []
    for i in range(m):
        p = (d*p + ord(pat[i])) % q
        ts = (d*ts + ord(txt2[i])) % q
    for s in range(k*k -2*k):
        if p == ts:
            match = True
            for i in range(m):
                if pat[i] != txt2[i+s]:
                    match  = False
                    break
            if match and txt2[s+k] == 'B' and txt2[s+k*2] == 'C':
                result.append(s)
                o+=1
        if s < n - m:
            ts = (ts - h * ord(txt2[s])) % q
            ts = (ts * d + ord(txt2[s+m])) % q
            ts = (ts + q) % q
    print("tyle ", o)
    return result

elapsed_time = time.time() - start_time

print(rabin(txt2, pat, 257, 11, k))
print(elapsed_time)
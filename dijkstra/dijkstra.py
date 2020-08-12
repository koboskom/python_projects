nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
distances = {
    'B': {'A': 5, 'D': 1, 'G': 2},
    'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
    'G': {'B': 2, 'D': 1, 'C': 2},
    'C': {'G': 2, 'E': 1, 'F': 16},
    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
    'F': {'A': 5, 'E': 2, 'C': 16}}

for i in distances:
    print(i, distances[i])

nieodwiedzone = {node: None for node in nodes}
odwiedzone = {}
startowy = input("podaj od ktorego wezla zaczynamy ")
Tdystans = 0
nieodwiedzone[startowy] = Tdystans

while True:

   for sasiad , dystans in distances[startowy].items():

       if sasiad not in nieodwiedzone: continue
       nowydystans = Tdystans + dystans

       if nieodwiedzone[sasiad] is None or nieodwiedzone[sasiad] > nowydystans:
           nieodwiedzone[sasiad] = nowydystans

   odwiedzone[startowy] = Tdystans
   del nieodwiedzone[startowy]
   print(nieodwiedzone)
   if not nieodwiedzone: break
   kandydat = [node for node in nieodwiedzone.items() if node[1]]
   startowy, Tdystans = sorted(kandydat, key = lambda x : x[1])[0]

print(odwiedzone)

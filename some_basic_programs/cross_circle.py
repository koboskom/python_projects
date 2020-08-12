table = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def rysuj():
    print("- - - - - - -")
    print("| {0} | {1} | {2} |".format(table[0], table[1], table[2]))
    print("| {0} | {1} | {2} |".format(table[3], table[4], table[5]))
    print("| {0} | {1} | {2} |".format(table[6], table[7], table[8]))
    print("- - - - - - -")
def  check():
    if (table[0]==table[1]==table[2]==('X' or '0')):
        print("win")
    if (table[3]==table[4]==table[5]==('X' or '0')):
        print("win")
    if (table[6]==table[7]==table[8]==('X' or '0')):
        print("win")
    if (table[0]==table[4]==table[8]==('X' or '0')):
        print("win")
    if (table[6]==table[4]==table[2]==('X' or '0')):
        print("win")
    if (table[0]==table[3]==table[6]==('X' or '0')):
        print("win")
    if (table[1]==table[4]==table[7]==('X' or '0')):
        print("win")
    if (table[2]==table[5]==table[8]==('X' or '0')):
        print("win")



rysuj()
for x in range (0,9):
    poz = int(input("podaj pozycje: "))
    if (table[poz-1] == ' '):
        table[poz-1] = 'X'

    rysuj()
    check()

    poz = int(input("podaj pozycje: "))
    if (table[poz - 1] == ' '):
        table[poz - 1] = '0'
    rysuj()
    check()

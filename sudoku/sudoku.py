board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def function_solver(matrix):

    find = find_empty(matrix)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(matrix, i, (row, col)):
            matrix[row][col] = i

            if function_solver(matrix):
                return True

            matrix[row][col] = 0

    return False


def valid(matrix, number, position):

    for i in range(len(matrix[0])):
        if matrix[position[0]][i] == number and position[1] != i:
            return False

    for i in range(len(matrix)):
        if matrix[i][position[1]] == number and position[0] != i:
            return False

    xbox = position[1] //3
    ybox = position[0] //3

    for i in range(ybox * 3, ybox * 3 + 3):
        for j in range(xbox * 3, xbox * 3 + 3):
            if matrix[i][j] == number and (i, j) != position:
                return False

    return True


def show(matrix):
    for i in range(len(matrix)):
        if i % 3 == 0 and i != 0:
            print ("- - - - - - - - - - - -")

        for j in range(len(matrix[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(matrix[i][j])
            else:
                print(str(matrix[i][j]) + " ", end="")


def find_empty(matrix):

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                return (i, j)

    return None


show(board)
function_solver(board)
print("--------------------------")
show(board)
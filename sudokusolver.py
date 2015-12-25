import re

# Five lists are used to by the backtracking algorithm to solve the sudoku
# puzzle:
#
# matrix - [matrix] is a list of length 81 where [matrix[i]] corresponds to the
# number on the sudoku puzzle in the ith position (the mapping of indices to
# positions is depicted below). An blank spot in the puzzle is represented by a
# [0] and the [0]s will gradually be replaced with other numbers as the
# algorithm solves the puzzle.
#
#   [ 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  ]
#   [ 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 ]
#   [ 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 ]
#   [ 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 ]
#   [ 36 | 37 | 38 | 39 | 40 | 41 | 42 | 43 | 44 ]
#   [ 45 | 46 | 47 | 48 | 49 | 50 | 51 | 52 | 53 ]
#   [ 54 | 55 | 56 | 57 | 58 | 59 | 60 | 61 | 62 ]
#   [ 63 | 64 | 65 | 66 | 67 | 68 | 69 | 70 | 71 ]
#   [ 72 | 73 | 74 | 75 | 76 | 77 | 78 | 79 | 80 ]
#
# binarymatrix - [binarymatrix] is a list of length 81 where [binarymatrix[i]]
# is [True] if number in the ith position was given by the original puzzle and
# [False] if otherwise (the mapping of indices to positions is the same as that
# of [matrix]). That is, [binarymatrix] distinguishes numbers produced by the
# algorithm with numbers given by the puzzle. [binarymatrix] is never modified
# by the algorithm.
#
# rowset - [rowset] is a list of length 9 where [rowset[i]] corresponds to the
# ith row of the sudoku puzzle (the mapping of indices to rows is depicted
# below). [rowset[i]] is a list of length 10 and acts as a set that shows
# whether or not a given number can be found on the ith row. So [rowset[i][j]]
# is [True] if the number [j] can be found on the ith row of the matrix. The
# list is of length 10 so that the indices align (index 0 is unused and indices
# 1 - 9 correspond to that particular number).
#    _________________
#   |_________________| 0
#   |_________________| 1
#   |_________________| 2
#   |_________________| 3
#   |_________________| 4
#   |_________________| 5
#   |_________________| 6
#   |_________________| 7
#   |_________________| 8
#
# colset - [colset] is the same as [rowset] but it is used for the columns of
# the sudoku puzzle. The mapping of indices to columns is depicted below.
#    _________________
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   | | | | | | | | | |
#   |_|_|_|_|_|_|_|_|_|
#    0 1 2 3 4 5 6 7 8
#
# boxset - [boxset] is the same as [rowset] but it is used for the boxes of
# the sudoku puzzle. The mapping of indices to boxes is depicted below.
#    _________________
#   |     |     |     |
#   |  0  |  1  |  2  |
#   |_____|_____|_____|
#   |     |     |     |
#   |  3  |  4  |  5  |
#   |_____|_____|_____|
#   |     |     |     |
#   |  6  |  7  |  8  |
#   |_____|_____|_____|

BOX_SIZE = 3
ROW_SIZE = BOX_SIZE * BOX_SIZE
BOX_ROW = BOX_SIZE * ROW_SIZE
MATRIX_SIZE = ROW_SIZE * ROW_SIZE

def print_matrix(matrix, size):
    """ Precondition:
            [size] is a nonnegative integer
            [matrix] is a list of length [size] * [size]
        Postcondition:
            Prints [matrix] in a readable format. [matrix] represents a matrix
            of row length [size].
    """
    for i in range(size):
        ind = i * size
        print("["),
        for j in range(size - 1):
            print(matrix[ind + j]),
            print("|"),
        print(matrix[ind + size - 1]),
        print("]")
    print("")

def mark(rowset, colset, boxset, ind, num, val):
    rowset[ind / ROW_SIZE][num] = val
    colset[ind % ROW_SIZE][num] = val
    boxset[BOX_SIZE * (ind / BOX_ROW) + ind % ROW_SIZE / BOX_SIZE][num] = val

def check_conflict(rowset, colset, boxset, ind, num):
    return (
        rowset[ind / ROW_SIZE][num] or
        colset[ind % ROW_SIZE][num] or
        boxset[BOX_SIZE * (ind / BOX_ROW) + ind % ROW_SIZE / BOX_SIZE][num]
    )

def initialize():
    """Creates and initializes the 5 lists as well as the prompt string and
    regex pattern."""
    matrix, binarymatrix, rowset, colset, boxset = [], [], [], [], []
    for i in range(MATRIX_SIZE):
        matrix.append(0)
        binarymatrix.append(False)
    for i in range(ROW_SIZE):
        rline, cline, bline = [], [], []
        for j in range(ROW_SIZE + 1):
            rline.append(False)
            cline.append(False)
            bline.append(False)
        rowset.append(rline)
        colset.append(cline)
        boxset.append(bline)
    p = re.compile('^[0-9]$')
    prompt = (
        "Enter the sudoku puzzle from left to right, top to bottom. Non-empty e"
        "ntries\n(boxes with numbers) are represented with the corresponding nu"
        "mber from 1-9.\nEmpty entries (empty boxes) can be represented with th"
        "e number 0. All other\ncharacters and whitespace will be ignored.\n\n"
    )
    return (p, prompt, matrix, binarymatrix, rowset, colset, boxset)

def prompt((p, prompt, matrix, binarymatrix, rowset, colset, boxset)):
    """Repeatedly prompts the user until a valid sudoku puzzle is inputed. The
    finalized lists are returned."""
    puzzle = raw_input(prompt)
    puzzle = [int(char) for char in puzzle if p.match(char)]
    if len(puzzle) > MATRIX_SIZE:
        print "Too many digits were passed. Please reenter the puzzle."
        return prompt((p, prompt, matrix, binarymatrix, rowset, colset, boxset))
    if len(puzzle) < MATRIX_SIZE:
        print "Too few digits were passed. Please reenter the puzzle."
        return prompt((p, prompt, matrix, binarymatrix, rowset, colset, boxset))
    for (i, num) in enumerate(puzzle):
        if num != 0:
            matrix[i] = num
            binarymatrix[i] = True
            mark(rowset, colset, boxset, i, num, True)
    return (matrix, binarymatrix, rowset, colset, boxset)

def backtrack_solve((matrix, binarymatrix, rowset, colset, boxset)):
    """Returns the solved sudoku puzzle as a list of the form [matrix]."""
    i, n = 0, 1
    while i < MATRIX_SIZE:
        if binarymatrix[i]:
            i += 1
            continue
        while n < 10 and check_conflict(rowset, colset, boxset, i, n):
            n += 1
        if n == 10:
            i -= 1
            while binarymatrix[i]:
                i -= 1
            n = matrix[i]
            mark(rowset, colset, boxset, i, n, False)
            n += 1
        else:
            matrix[i] = n
            mark(rowset, colset, boxset, i, n, True)
            i += 1
            n = 1
    return matrix

print_matrix(backtrack_solve(prompt(initialize())), ROW_SIZE)
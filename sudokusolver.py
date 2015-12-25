import re

def printmatrix(matrix):
	for i in range(9):
		print("["),
		for j in range(8):
			print(matrix[i*9+j]),
			print("|"),
		print(matrix[i*9+j+1]),
		print("]")
	print("")

def assignbox(index, num, val):
	boxset[3 * (index / 27) + index % 9 / 3][num] = val

def getbox(index, num):
	return boxset[3 * (index / 27) + index % 9 / 3][num]

p = re.compile('^[0-9]$')
matrix = []
binarymatrix = []
rowset = []
colset = []
boxset = []
for i in range(81):
	matrix.append(0)
	binarymatrix.append(False)
for i in range(9):
	rline = []
	cline = []
	bline = []
	for j in range(10):
		rline.append(False)
		cline.append(False)
		bline.append(False)
	rowset.append(rline)
	colset.append(cline)
	boxset.append(bline)

puzzle = raw_input("""Enter the sudoku puzzle from left to right, top to bottom. Non-empty entries (boxes with numbers) 
are represented with the corresponding number from 1-9. Empty entries (empty boxes) can be represented with 
the number 0. All other characters and whitespace is ignored.
""")
i = 0
for char in puzzle:
	if(i==81):
		break
	if(p.match(char)):
		num = int(char)
		if(num == 0):
			i+=1
		else:
			matrix[i] = num
			binarymatrix[i] = True
			rowset[i/9][num] = True
			colset[i%9][num] = True
			assignbox(i, num, True)
			i+=1

i = 0
n = 1
while(i<81):
	if(binarymatrix[i]):
		i += 1
		continue
	while(n<10 and (rowset[i/9][n] or colset[i%9][n] or getbox(i, n))):
		n += 1
	if(n==10):
		i -= 1
		while(binarymatrix[i]):
			i -= 1
		n = matrix[i]
		rowset[i/9][n] = False
		colset[i%9][n] = False
		assignbox(i, n, False)
		n += 1
	else:
		matrix[i] = n
		rowset[i/9][n] = True
		colset[i%9][n] = True
		assignbox(i, n, True)
		i += 1
		n = 1

printmatrix(matrix)
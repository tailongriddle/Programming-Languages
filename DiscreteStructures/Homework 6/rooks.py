
def buildBoard(constraints,size): 
    rows, cols = (size, size)
    board = [["o" for _ in range(cols)] for _ in range(rows)] # 2d list
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (i,j) in constraints:
                board[i][j] = "x"
                # print("CHANGE")
                # print((i,j))
            print(board[i][j], " ", end="")
        print(" ")
  
    return board

def shiftConstraints(constraints):
    shifted_constraints = []
    for x, y in constraints:
        shifted_constraints.append((x-1, y-1))
    print(shifted_constraints)
    return shifted_constraints

def probability(board,size):
    
    return 0

invalidCells = [(1,1),(5,5)]
size = 6

shiftedInvalid = shiftConstraints(invalidCells)
rookBoard = buildBoard(shiftedInvalid,size)





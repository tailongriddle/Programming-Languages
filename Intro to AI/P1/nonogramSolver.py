import time
def initialize_grid(n):
# create empty nonogram
    return [[0 for i in range(n)] for j in range(n)] # empty nonogram as

# print constraints
def print_constraints_and_puzzle(puzzle, rowConstraints, colConstraints):  
    max_col_constraints = max(len(x) for x in colConstraints) # find the maximum number of column constraints
    max_row_constraints = max(len(x) for x in rowConstraints) # find the maximum number of row constraints  
    
    # print the column constraints
    for i in range(max_col_constraints):
        for x in range(max_row_constraints):
            print(" ", end = "  ")
            
        for j in range(size): # iterate through the columns
            if max_col_constraints - i <= len(colConstraints[j]): 
                print(colConstraints[j][len(colConstraints[j]) - max_col_constraints + i], end = "  ") 
            else:
                print(" ", end = "  ")
        print() # print new line after each row of column constraints
 
    for i in range(size):
        for x in range(max_row_constraints - len(rowConstraints[i])):
            print(" ", end = "  ")
        print(rowConstraints[i], end = "  ") # print row constraints
        for j in range(size):
            if puzzle[i][j] == 1:
                print("X", end = "  ") # print filled cell as "X"
            elif puzzle[i][j] == -1:
                print(" ", end = "  ") # print empty cell as space
            else:
                print("0", end = "  ")
        print() # print new line after each row

    
# initial forward propogation of hard constraints
# fill cells starting from the middle based on constraints
# for example, a column constraint [10] for a column would fill the entire column
# a row constraint [8] would definitely fill the middle 6 cells of the row
def set_filled_cells(puzzle, rowConstraints, colConstraints):
    size = len(puzzle)
           
    # if row constraint is more than half of the size of the puzzle, put the filled cells in the middle
    # filled cells will be centered and the number of filled cells will be equal to (rowConstraint - (size // 2) ) * 2
    for i in range(size):
        if len(rowConstraints[i]) == 1:
            if rowConstraints[i][0] > size // 2:
                filled_cells = (rowConstraints[i][0] - (size // 2)) * 2
                start = (size - filled_cells) // 2
                for j in range(start, start + filled_cells):
                    puzzle[i][j] = 1
                
    # if column constraint is more than half of the size of the puzzle, put the filled cells in the middle
    # filled cells will be centered and the number of filled cells will be equal to (colConstraint - (size // 2)) * 2
    for j in range(size):
        if len(colConstraints[j]) == 1:
            if colConstraints[j][0] > size // 2:
                filled_cells = (colConstraints[j][0] - (size // 2)) * 2
                start = (size - filled_cells) // 2
                for i in range(start, start + filled_cells):
                    puzzle[i][j] = 1

# set empty cells based on constraints
# if the current filled cells are away from the border by more than the amount in the constraint, fill the cells that MUST be empty
def set_empty_cells(puzzle, rowConstraints, colConstraints):                  
    #rows
    for i in range(size):
        row_filled = sum(1 for x in puzzle[i] if x == 1) # number of filled cells in the row
        
        # make empty cells that should be empty because no more space left
        for j in range(size):
            if puzzle[i][j] == 0:  # check whether this should be empty based on the constraints
                if len(rowConstraints[i]) == 1:
                    if row_filled == rowConstraints[i][0]:  # out of room 
                        puzzle[i][j] = -1  # mark as empty
    #columns
    for j in range(size):
        col_filled = sum(1 for x in range(size) if puzzle[x][j] == 1) # number of filled cells in the column
        
        # make empty cells that should be empty because no more space left
        for i in range(size): 
            if len(colConstraints[j]) == 1:
                if puzzle[i][j] == 0:
                    if col_filled > colConstraints[j][0]:  # out of room 
                        puzzle[i][j] = -1  # mark as empty
                                  
   
def solve_nonogram(puzzle, rowConstraints, colConstraints):
    if is_solved(puzzle):
        return puzzle
    
    size = len(puzzle)
    
    # find the first empty cell
    for i in range(size): # iterate through the rows
        for j in range(size): # iterate through the columns
            if puzzle[i][j] == 0: # empty cell
                break
        if puzzle[i][j] == 0: #
            break
        
    # try filling the cell
    for value in [1, -1]:
        puzzle[i][j] = value
        if is_valid_assignment(puzzle, rowConstraints, colConstraints):
            result = solve_nonogram(puzzle, rowConstraints, colConstraints)
            if result:
                print("solution found")
                return result
            puzzle[i][j] = 0  # backtrack

    puzzle[i][j] = 0  # backtrack
    return None
        
def is_valid_assignment(puzzle, rowConstraints, colConstraints):
    size = len(puzzle)
    # check if the row constraints are satisfied
    for i in range(size):
        if not is_valid_row(puzzle[i], rowConstraints[i]):
            return False
    # check if the column constraints are satisfied
    for j in range(size):
        col = [puzzle[i][j] for i in range(size)]
        if not is_valid_col(col, colConstraints[j]):
            return False
    return True

def is_valid_row(row, constraints):
    # invalid if number of filled cells in row > the sum of the constraints
    # invalid if block of filled cells is at any point more than any num in constraint list
    # invalid if there is no empty space between num of filled cells stated in constraints
    blocks = []
    filled_cells = 0
    for cell in row:
        if cell == 1:  # filled cell
            filled_cells += 1
        elif cell == -1:  # empty cell
            if filled_cells > 0:
                blocks.append(filled_cells)
                filled_cells = 0
    if filled_cells > 0:
        blocks.append(filled_cells)
        
    # check if blocks match constraints
    if len(blocks) > len(constraints):
        return False
    for block, constraint in zip(blocks, constraints):
        if block > constraint:
            return False    
    return True

def is_valid_col(col, constraints):
    # invalid if number of filled cells in col > the sum of the constraints
    # invalid if block of filled cells is at any point more than any num in constraint list
    # invalid if there is no empty space between num of filled cells stated in constraints
    blocks = []
    filled_cells = 0
    for cell in col:
        if cell == 1:  # filled cell
            filled_cells += 1
        elif cell == -1:  # empty cell
            if filled_cells > 0:
                blocks.append(filled_cells)
                filled_cells = 0
    if filled_cells > 0:
        blocks.append(filled_cells)
        
    # check if blocks match constraints
    if len(blocks) > len(constraints):
        return False
    for block, constraint in zip(blocks, constraints):
        if block > constraint:
            return False    
    return True

        
    
    
# checks if puzzle is solved
def is_solved(puzzle):
    return all(cell != 0 for row in puzzle for cell in row)
               
# tree nonogram
# rowConstraints = [[2], [2], [4], [2], [6], [4], [8], [2], [2], [2]]
# colConstraints = [[0], [1], [1,1], [1,3], [10], [10], [1,3], [1,1], [1], [0]]

size = 6 # size of the nonogram

# diamond nonogram
# colConstraints = [[2], [4], [6], [6], [4], [2]]
# rowConstraints = [[2], [4], [6], [6], [4], [2]]

# square nonogram
# colConstraints = [[0], [4], [4], [4], [4], [0]]
# rowConstraints = [[0], [4], [4], [4], [4], [0]]

# triangle nonogram
colConstraints = [[1], [3], [5], [5], [3], [1]]
rowConstraints = [[2], [2], [4], [4], [6], [0]]

# rectangle nonogram
# colConstraints = [[0], [6], [6], [6], [6], [0]]
# rowConstraints = [[4], [4], [4], [4], [4], [4]]

puzzle = initialize_grid(size)

#set_filled_cells(puzzle, rowConstraints, colConstraints)
#print_constraints_and_puzzle(puzzle, rowConstraints, colConstraints)
#set_empty_cells(puzzle, rowConstraints, colConstraints)
#print_constraints_and_puzzle(puzzle, rowConstraints, colConstraints)

print_constraints_and_puzzle(puzzle, rowConstraints, colConstraints)

start = time.time()

#Diamond Time Taken


i = 0

while i < 1000: 
    puzzle = initialize_grid(size)
    set_filled_cells(puzzle, rowConstraints, colConstraints)
    set_empty_cells(puzzle, rowConstraints, colConstraints)
    solution = solve_nonogram(puzzle, rowConstraints, colConstraints)
    i += 1
end = time.time()

average_time = (end - start) / 1000

if solution:
    print("\nSolved Puzzle:")
    print_constraints_and_puzzle(solution, rowConstraints, colConstraints)
else:
    print("No solution found!")
    
print("Average CSP time taken: ", average_time, "seconds.")

# 0.00012
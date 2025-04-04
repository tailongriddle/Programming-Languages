import itertools
import numpy as np
import time

# checks if the filled row matches the constraints
def is_valid_row(row, constraints):
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

    # Check if blocks match constraints
    if len(blocks) != len(constraints):
        return False
    for block, constraint in zip(blocks, constraints):
        if block != constraint:
            return False
    return True

# checks if the filled column matches the constraints
def is_valid_col(col, constraints):
    blocks = [] # list of blocks of filled cells
    filled_cells = 0 # number of filled cells in the block
    for cell in col: # for each cell in the column
        if cell == 1:  # filled cell
            filled_cells += 1 # increment the number of filled cells in the block
        elif cell == -1:  # empty cell
            if filled_cells > 0: # if there are filled cells in the block
                blocks.append(filled_cells) # add the number of filled cells in the block to the list of blocks
                filled_cells = 0 # reset number of filled cells in the block
    if filled_cells > 0:
        blocks.append(filled_cells)

    # check if blocks match constraints
    if len(blocks) != len(constraints): # if the number of blocks in the column != to the number of constraints
        return False
    for block, constraint in zip(blocks, constraints): # check if the number of filled cells in each block matches the constraints
        if block != constraint: # if the number of filled cells in the block is not equal to the constraint
            return False    
    return True

# generates valid rows
def generate_valid_rows(size, row_constraints):
    valid_rows = []
    for constraints in row_constraints:
        possible_rows = []
        for row in itertools.product([-1, 1], repeat=size):
            if is_valid_row(row, constraints):
                possible_rows.append(row)
        valid_rows.append(possible_rows)
    return valid_rows

# checks if the grid satisfies all column constraints
def is_valid_grid(grid, col_constraints):
    size = len(grid)
    for col_index in range(size):
        col = [grid[row_index][col_index] for row_index in range(size)]
        if not is_valid_col(col, col_constraints[col_index]):
            return False
    return True

# nonogram solver (brute force)
def solve_nonogram(row_constraints, col_constraints):
    size = len(row_constraints)  
    
    # generates all valid row configurations
    valid_rows = generate_valid_rows(size, row_constraints)
    #print("Valid rows:", valid_rows)
    # try all combinations of valid rows to form a valid grid
    for row_combination in itertools.product(*valid_rows):
        grid = np.array(row_combination)
        print("Grid:", grid)
        
        # check if the grid satisfies the column constraints
        if is_valid_grid(grid, col_constraints):
            return grid  # Return the solution if valid
    
    return None  # return None if no solution is found

# example nonogram constraints
# diamond nonogram
colConstraints = [[2], [4], [6], [6], [4], [2]]
rowConstraints = [[2], [4], [6], [6], [4], [2]]

# square nonogram
# colConstraints = [[0], [4], [4], [4], [4], [0]]
# rowConstraints = [[0], [4], [4], [4], [4], [0]]

# triangle nonogram
# colConstraints = [[1], [3], [5], [5], [3], [1]]
# rowConstraints = [[2], [2], [4], [4], [6], [0]]

# rectangle nonogram
# colConstraints = [[0], [6], [6], [6], [6], [0]]
# rowConstraints = [[4], [4], [4], [4], [4], [4]]

# solve the Nonogram
i = 0
start = time.time()
while i < 1000: 
    solution = solve_nonogram(rowConstraints, colConstraints)
    i += 1

end = time.time()

average_time = (end - start) / 1000
# print the solution if found
if solution is not None:
    print("Solution:")
    print(solution)
else:
    print("No solution found.")

print("Average brute time taken:", average_time, "seconds.")
"""

CS571 : Assignment 1
Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

"""

# Import Libraries
from collections import deque
import random
import time


# Generating initial random grid
# returns a random 3*3 grid for sliding puzzle


def generate_random_grid():
    # List of numbers and 'B' to represent the puzzle grid
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 'B']
    random.shuffle(numbers)

    # Construct the 3*3 grid
    random_grid = ((numbers[0], numbers[1], numbers[2]), (numbers[3],
                   numbers[4], numbers[5]), (numbers[6], numbers[7], numbers[8]))

    return random_grid


# Check if the puzzle is solvable by Conting Inversions
# If inversion are odd we can't solve,If they are even we can solve the puzzle


def is_Possible(grid):
    initial = [cell for row in grid for cell in row]
    ct = 0

    for x in range(len(initial)):
        for y in range(x+1, len(initial)):
            if initial[x] != 'B' and initial[y] != 'B' and (initial[x] > initial[y]):
                ct += 1

    # returns True if solvable,False if not.
    return ct % 2 == 0


# To check index of row and column is valid or not


def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Swap function to move the blank space 'B'


def swap(grid, x1, y1, x2, y2):
    new_grid = [list(row) for row in grid]
    new_grid[x1][y1], new_grid[x2][y2] = new_grid[x2][y2], new_grid[x1][y1]
    return tuple(map(tuple, new_grid))

# BFS


def bfs(start, target):
    state_explored = 0
    queue = deque([(start, 0)])
    visited = set([start])

    while queue:
        state_explored += 1
        current, steps = queue.popleft()

        # If we can reach the target return True(That we have reached) and number of steps required.
        if current == target:
            return True, steps, state_explored

        x, y = 0, 0
        # Find the position of the blank space 'B'
        for i in range(3):
            for j in range(3):
                if current[i][j] == 'B':
                    x, y = i, j

        # directions right,left,down and up
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                new_grid = swap(current, x, y, nx, ny)
                if new_grid not in visited:
                    visited.add(new_grid)
                    queue.append((new_grid, steps + 1))

    # if we can't react the target return False
    return False, 0, state_explored

# DFS


def dfs(start, target):
    state_explored = 0
    stack = [(start, 0)]
    visited = set([start])

    while stack:
        state_explored = state_explored+1
        current,  steps = stack.pop()

        # If we can reach the target return True(That we have reached) and number of steps required.
        if current == target:
            return True, steps, state_explored

        x, y = 0, 0
        # Find the position of the blank space 'B'
        for i in range(3):
            for j in range(3):
                if current[i][j] == 'B':
                    x, y = i, j

        # directions right,left,down and up
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                new_grid = swap(current, x, y, nx, ny)
                if new_grid not in visited:
                    visited.add(new_grid)
                    stack.append((new_grid, steps + 1))

    # if we can't react the target return False
    return False, 0, state_explored


# solve puzzle using BFS and DFS and return number of steps required
def solve_puzzle(start, target, search_type="bfs"):
    if search_type == "bfs":
        found, num_steps, state_explored = bfs(start, target)
    elif search_type == "dfs":
        found,  num_steps, state_explored = dfs(start, target)

    return found, num_steps, state_explored

# -------------------------------------------------------------------------------------------------------------------------------------#


# Generating random start grid
start_grid = generate_random_grid()

# Print the starting grid
print("\nStart grid is:")
for row in start_grid:
    print(row)

# Target Grid
target_grid = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 'B')
)


# Check if puzzle is solvable
# if yes solve the puzzle

if (is_Possible(start_grid)):

    # solve using BFS
    start_bfs = time.time()
    found_bfs, num_steps_bfs, state_explored_bfs = solve_puzzle(
        start_grid, target_grid, search_type="bfs")
    end_bfs = time.time()

    if found_bfs:
        print("\nBFS:")
        print("No. of moves:", num_steps_bfs)
        print("Stated Explored: ", state_explored_bfs)
        print("Time taken by BFS:", round(end_bfs-start_bfs, 5))
    else:
        print("\nCannot reach the target using BFS.")

    # solve using DFS
    start_dfs = time.time()
    found_dfs, num_steps_dfs, state_explored_dfs = solve_puzzle(
        start_grid, target_grid, search_type="dfs")
    end_dfs = time.time()

    if found_dfs:
        print("\nDFS:")
        print("No. of moves: ", num_steps_dfs)
        print("Stated Explored: ", state_explored_dfs)
        print("Time taken by DFS:", round(end_dfs-start_dfs, 5))
    else:
        print("\nCannot reach the target using DFS.")

else:
    print("\nCannot reach the target.")

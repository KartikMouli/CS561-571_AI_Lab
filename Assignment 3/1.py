"""

CS571 : Assignment 3
Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

"""

# Import Libraries
from collections import deque
import random
import time
import heapq

# Assumption Black Space B is represented by 0.

# generate random grid


def generate_random_grid():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(numbers)
    random_grid = ((numbers[0], numbers[1], numbers[2]),
                   (numbers[3], numbers[4], numbers[5]),
                   (numbers[6], numbers[7], numbers[8]))
    return random_grid


# check if puzzle is solvable using count inversion


def is_Possible(grid):
    initial = [cell for row in grid for cell in row]
    ct = 0
    for x in range(len(initial)):
        for y in range(x + 1, len(initial)):
            if initial[x] != 0 and initial[y] != 0 and (initial[x] > initial[y]):
                ct += 1
    return ct % 2 == 0

# check if we are doing a valid move


def is_valid(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# function to swap cells


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
        # Find the position of the blank space 0
        for i in range(3):
            for j in range(3):
                if current[i][j] == 0:
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
        # Find the position of the blank space 0
        for i in range(3):
            for j in range(3):
                if current[i][j] == 0:
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

# UCS


def ucs(start, target):
    state_explored = 0
    pq = [(0, start, 0)]
    visited = set([start])

    while pq:
        cost, current, steps = heapq.heappop(pq)  # using priority queue
        state_explored += 1

        if current == target:                       # If goal state found return True
            return True, steps, state_explored

        x, y = 0, 0
        for i in range(3):
            for j in range(3):
                if current[i][j] == 0:
                    x, y = i, j

        # directions for swapping
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if is_valid(nx, ny):
                new_grid = swap(current, x, y, nx, ny)
                if new_grid not in visited:
                    visited.add(new_grid)
                    heapq.heappush(pq, (cost + 1, new_grid, steps + 1))

    return False, 0, state_explored


# IDS


def ids(start, target):
    max_depth = 0  
    state_explored = 0      # current maximum depth
    while True:
        stack = [(start, 0)]  # stack to store states
        visited = set([start])  # store visited states
        while stack:
            current, steps = stack.pop()
            state_explored += 1

            if current == target:           # If goal state found return True
                return True, steps, state_explored

            if steps <= max_depth:
                x, y = 0, 0
                for i in range(3):
                    for j in range(3):
                        if current[i][j] == 0:
                            x, y = i, j

                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy

                    if is_valid(nx, ny):
                        new_grid = swap(current, x, y, nx, ny)
                        if new_grid not in visited:
                            visited.add(new_grid)
                            stack.append((new_grid, steps + 1))

        max_depth += 1


# -----------------------------------------------------------------------------------------------------------------------------------------------#

# print randomly generated start grid
start_grid = generate_random_grid()

print("\nStart grid is:")
for row in start_grid:
    print(row)

# target grid
target_grid = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

# check if it is possble to solve the puzzle
if is_Possible(start_grid):

    # solve using BFS
    start_bfs = time.time()
    found_bfs, num_steps_bfs, state_explored_bfs = bfs(start_grid, target_grid)
    end_bfs = time.time()

    print("\nBFS: ")
    print("No. of moves:\t", num_steps_bfs)
    print("Stated Explored:", state_explored_bfs)
    print("Time taken:\t", round(end_bfs-start_bfs, 5), "seconds")

    # solve using DFS
    start_dfs = time.time()
    found_dfs, num_steps_dfs, state_explored_dfs = dfs(start_grid, target_grid)
    end_dfs = time.time()

    print("\nDFS: ")
    print("No. of moves:\t", num_steps_dfs)
    print("Stated Explored:", state_explored_dfs)
    print("Time taken:\t", round(end_dfs-start_dfs, 5), "seconds")

    # solve using UCS
    start_ucs = time.time()
    found_ucs, num_steps_ucs, state_explored_ucs = ucs(start_grid, target_grid)
    end_ucs = time.time()

    print("\nUCS: ")
    print("No. of moves:\t", num_steps_ucs)
    print("Stated Explored:", state_explored_ucs)
    print("Time taken:\t", round(end_ucs-start_ucs, 5), "seconds")

    # solve using IDS
    start_ids = time.time()
    found_ids, num_steps_ids, state_explored_ids = ids(
        start_grid, target_grid)
    end_ids = time.time()

    print("\nIDS: ")
    print("No. of moves:\t", num_steps_ids)
    print("Stated Explored:", state_explored_ids)
    print("Time taken:\t", round(end_ids-start_ids, 5), "seconds")

    # Compare the algorithms
    algorithm_steps = {
        "Uniform Cost Search": num_steps_ucs,
        "Iterative Deepening Search": num_steps_ids,
        "Breadth-First Search": num_steps_bfs,
        "Depth-First Search": num_steps_dfs
    }

    # print optimal algo ( metric : #steps required)
    min_steps = min(algorithm_steps.values())
    optimal_algo = []
    print("\nOptimal Algorith(s) with ",
          "\033[1m", min_steps, "steps \033[0m is/are: ", end=" ")
    for name, steps in algorithm_steps.items():
        if (steps == min_steps):
            optimal_algo.append(name)

    for i in range(len(optimal_algo)):
        print("\033[1m", optimal_algo[i], "\033[0m", end="")
        if i < len(optimal_algo) - 1:
            print(", ", end="")

else:
    print("\nCannot reach the target.")

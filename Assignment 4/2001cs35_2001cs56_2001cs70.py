"""

CS571 : Assignment 4
Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

"""

import numpy as np
import time
from queue import PriorityQueue

# Define the heuristic functions h1 and h2


def h1(state):
    return np.sum(state != goal_state)


def h2(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i, j]
            goal_i, goal_j = np.where(goal_state == val)
            distance += abs(i - goal_i) + abs(j - goal_j)
    return distance


# Get neighboring states by swapping the empty tile
def get_neighbors(state):
    neighbors = []
    empty_i, empty_j = np.where(state == 0)
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = empty_i + di, empty_j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = state.copy()
            new_state[empty_i, empty_j], new_state[ni,
                                                   nj] = new_state[ni, nj], new_state[empty_i, empty_j]
            neighbors.append(new_state)
    return neighbors


# Hill Climbing algorithm


def hill_climbing(initial_state, heuristic):
    visited = set()
    queue = PriorityQueue()
    unique_id = 0  # Counter for creating unique identifiers
    total_states_explored = 0  # Counter for total states explored

    # Put the initial state in the priority queue
    queue.put((heuristic(initial_state), unique_id,
              initial_state, [initial_state], 0))
    unique_id += 1

    while not queue.empty():
        _, _, current_state, path, cost = queue.get()
        if np.array_equal(current_state, goal_state):
            return True, path, cost, total_states_explored  # If goal State frond then return

        visited.add(tuple(current_state.reshape(-1)))  # add to visited
        total_states_explored += 1
        neighbors = reversed(get_neighbors(current_state)
                             )  # get neighbouring states

        for neighbor in neighbors:
            if tuple(neighbor.reshape(-1)) not in visited:
                new_cost = cost + 1
                queue.put((heuristic(neighbor), unique_id,
                          neighbor, path + [neighbor], new_cost))
                unique_id += 1

    # if goal state not found return false
    return False, None, None, total_states_explored


# Function to read the state from a line in the input file
def read_state_from_line(line, str_to_num):
    state = line.strip().split(',')
    state = [str_to_num[item] for item in state]
    return np.array(state).reshape(3, 3)


if __name__ == "__main__":

    # dictionaty to map str to int and vice versa
    str_to_num = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4,
                  'T5': 5, 'T6': 6, 'T7': 7, 'T8': 8, 'B': 0}

    num_to_str = {1: 'T1', 2: 'T2', 3: 'T3', 4: 'T4',
                  5: 'T5', 6: 'T6', 7: 'T7', 8: 'T8', 0: 'B'}

    # Choose the heuristic function (h1 or h2)
    heuristics = [[h1, 1, "Number of tiles displaced from their destined position"], [
        h2, 2, "sum of the Manhattan distance of each tile from the goal position"]]

    # Read the input file
    with open('puzzle_input.txt', 'r') as file:
        initial_state_line = next(
            line for line in file if line.strip() and not line.startswith('#')).strip()
        goal_state_line = next(line for line in file if line.strip()
                               and not line.startswith('#')).strip()

    # Convert the lines to arrays
    initial_state = read_state_from_line(initial_state_line, str_to_num)
    goal_state = read_state_from_line(goal_state_line, str_to_num)

    # Loop through heuristics and run the Hill Climbing algorithm
    for h, i, j in heuristics:
        # Run the Hill Climbing algorithm
        start_time = time.time()
        found_solution, optimal_path, path_cost, states_explored = hill_climbing(
            initial_state, h)
        end_time = time.time()

        # print desired output
        print("\nFor Heuristic h"+str(i), '(', j, '):')
        if found_solution:
            print("Success !")
            print("\nIntital State:")
            print('\n'.join(
                ['  '.join([f'{num_to_str[tile]:<2}' for tile in row]) for row in initial_state]))
            print("\nGoal State:")
            print('\n'.join(
                ['  '.join([f'{num_to_str[tile]:<2}' for tile in row]) for row in goal_state]))
            print("\nTotal No. of States Explored: ", states_explored)
            print("Total No. of states to optimal path: ", len(optimal_path))
            # print("Optimal Path:")
            # for state in optimal_path:
            #     print('\n'.join(
            #         ['  '.join([f'{num_to_str[tile]:<2}' for tile in row]) for row in state]))
            #     print()
            print("Path Cost:", path_cost)
            print("Time taken for execution: ", round(
                end_time-start_time, 5), "sec")
        else:
            print("Failure !")
            print("\nIntital State:")
            print(initial_state)
            print("\nGoal State:")
            print(goal_state)
            print("Total number of states explored before termination: ",
                  states_explored)
            print("Time taken for execution: ", round(
                end_time-start_time, 5), "sec")

        if (i == 1):
            print("\n----------------------------------------------------------------------------------------------------")

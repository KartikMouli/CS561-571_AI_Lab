"""

CS571 : Assignment 5
Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

"""

# importing packages
import numpy as np
import random
import math
import time

# fxn to check whether the current coordinates are within the bounds


def check(x, y):
    if x < 0 or y < 0 or x > 2 or y > 2:
        return 1
    return 0

# first heuristic for count of displaced tiles


def displaced(cur_state, final_state, blank):
    displaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if cur_state[i][j] == 0 and not blank:
                continue
            if cur_state[i][j] != final_state[i][j]:
                displaced_tiles += 1
    return displaced_tiles

# second heuristic for manhattan distance of each tile from actual pos


def manhattan(cur_state, final_state, blank):
    manhattan_dis = 0
    for c_i in range(3):
        for c_j in range(3):
            value = cur_state[c_i][c_j]
            if value == 0 and not blank:
                continue
            e_i = int((value - 1) / 3)
            e_j = (value - 1) % 3
            manhattan_dis += abs(e_i - c_i) + abs(e_j - c_j)
    return manhattan_dis

# common heuristic function


def heuristic(h, cur_state, final_state, blank):
    if h == "h1":
        return displaced(cur_state, final_state, blank)
    elif h == 'h2':
        return manhattan(cur_state, final_state, blank)

# finding the position of blank tile


def pos(cur_state):
    state = np.array(cur_state)
    temp = np.where(state == 0)
    return temp[0][0], temp[1][0]


# list defined to store 4 dirns of possible swaps
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

# stores the optimal vost
optimal_cost = {}

# for finding the most efficient solution, so that we can check addmissibility of the heuristics


def bfs(initial_state, final_state, initial_pos):
    visited, queue_state, queue_moves, queue_pos = set(), [initial_state], [
        0], [initial_pos]
    optimal_cost[initial_state] = 0
    visited.add(initial_state)
    while queue_state:
        cur_state = queue_state.pop(0)
        cur_moves = queue_moves.pop(0)
        cur_pos = queue_pos.pop(0)
        if cur_state == final_state:
            print(f'Solution exists')
            break
        for i in range(4):
            new_x = cur_pos[0] + dx[i]
            new_y = cur_pos[1] + dy[i]
            if(check(new_x, new_y)):
                continue

            new_state = cur_state
            new_state = list(map(list, new_state))
            new_state[cur_pos[0]][cur_pos[1]] = new_state[new_x][new_y]
            new_state[new_x][new_y] = 0
            new_state = tuple(map(tuple, new_state))

            if new_state not in visited:
                visited.add(new_state)
                queue_state.append(new_state)
                queue_moves.append(cur_moves + 1)
                queue_pos.append((new_x, new_y))
                optimal_cost[new_state] = cur_moves + 1

# fxn to solve the 8 puzzle using Simulated Annealing Search Algorithm
# temp. 10 -> 0.1 (at the rate of 0.000099) - iterations = 1e5


def simulated_annealing(initial_state, final_state, h, temperature, blank, rate):
    st = time.time()
    states_explored = 0
    cur_state = initial_state
    path_construct = {}
    path_cost = {}
    path_cost[cur_state] = 0
    admissible = True
    while temperature > 0.1:
        states_explored += 1
        cur_energy = heuristic(h, cur_state, final_state, blank)
        cur_pos = pos(cur_state)
        if cur_state == final_state:
            print(f'Heuristic: {h}\n')
            print(f'Final state Reached!')
            print(f'Total no. of states explored: {states_explored}')
            print(
                f'Total no. of states to the optimal path: {path_cost[cur_state] + 1}')
            print(f'Admissible or not: {admissible}')
            print(f'Optimal Cost: {path_cost[cur_state]}')
            print(f'Time taken for execution: {time.time() - st} seconds\n\n')
            # print("Optimal Path:")
            # for _ in path_construct:
            #     print(_)
            #     print()
            return

        new_states = []
        # calculating 4 new x,y
        for i in range(4):
            new_x = cur_pos[0] + dx[i]
            new_y = cur_pos[1] + dy[i]
            if check(new_x, new_y):
                continue

            # exchanging positions
            new_state = cur_state
            new_state = list(map(list, new_state))
            new_state[cur_pos[0]][cur_pos[1]] = new_state[new_x][new_y]
            new_state[new_x][new_y] = 0
            new_state = tuple(map(tuple, new_state))

            new_energy = heuristic(h, new_state, final_state, blank)
            if new_state in optimal_cost.keys() and new_energy > optimal_cost[new_state]:
                admissible = False
            new_states.append((new_energy, new_state))

        # when temperature hasn't reahed 0.1 yet
        while temperature > 0.1:
            temp = random.choice(new_states)
            new_state = temp[1]
            delta_energy = temp[0] - cur_energy
            # when delta E <=0
            if delta_energy <= 0:
                if new_state in path_cost:
                    path_cost[new_state] = min(
                        path_cost[new_state], path_cost[cur_state] + 1)
                else:
                    path_cost[new_state] = path_cost[cur_state] + 1
                path_construct[new_state] = cur_state
                cur_state = new_state
                temperature -= 0.000099
                break
            # when random no. <= probability generated
            else:
                prob = math.exp(-float(delta_energy)/temperature)
                temperature -= 0.000099
                r = random.uniform(0, 1)
                if r <= prob:
                    if new_state in path_cost:
                        path_cost[new_state] = min(
                            path_cost[new_state], path_cost[cur_state] + 1)
                    else:
                        path_cost[new_state] = path_cost[cur_state] + 1
                    path_construct[new_state] = cur_state
                    cur_state = new_state
                    break

    print(f'Heuristic: {h}')
    print(f'Final state not Reachable!')
    print(f'Total no. of states explored: {states_explored}\n\n')


def main():
    # Randomly generated initial state

    initial_state = np.arange(0, 9)
    # initial_state=np.array([1,3,8,0,2,6,5,7,4])
    np.random.shuffle(initial_state)
    initial_state = np.reshape(initial_state, (3, 3))
    initial_state = initial_state.tolist()
    final_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # printing the initial state
    print('Start State:')
    for i in range(3):
        for j in range(3):
            if initial_state[i][j]:
                print(f'{initial_state[i][j]} ', end='')
            else:
                print('B ', end='')
        print('\n')

    initial_state = tuple(map(tuple, initial_state))
    final_state = tuple(map(tuple, final_state))

    # calling Simulated Annealing Fxn multiple times to get results
    blank = False   # mean blank not to be considered another tile
    temperature = 10
    rate = 0.000099

    bfs(final_state, initial_state, pos(final_state))

    simulated_annealing(initial_state, final_state,
                        "h1", temperature, blank, rate)
    simulated_annealing(initial_state, final_state,
                        "h2", temperature, blank, rate)


if __name__ == "__main__":
    main()

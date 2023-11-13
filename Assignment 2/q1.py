import random
import time
import math

source_state = []
goal_state = []
inf = 1000000000


def generateRandomState():
    state = list(range(9))
    random.shuffle(state)
    return state


def h(state, des, heuristic):
    if heuristic == "manhattan":
        manhattan_dis = 0
        for tile in range(1, 9):
            for i_state in range(9):
                for i_des in range(9):
                    if state[i_state] == tile and des[i_des] == tile:
                        x_state, y_state = i_state // 3, i_state % 3
                        x_des, y_des = i_des // 3, i_des % 3
                        manhattan_dis += abs(x_state - x_des) + \
                            abs(y_state - y_des)
        return manhattan_dis
    elif heuristic == "displaced":
        displaced_tiles = sum(1 for i in range(
            9) if state[i] != 0 and state[i] != des[i])
        return displaced_tiles
    elif heuristic == "custom":
        custom_tiles = 0
        for tile in range(1, 9):
            for i_state in range(9):
                for i_des in range(9):
                    if state[i_state] == tile and des[i_des] == tile:
                        x_state, y_state = i_state // 3, i_state % 3
                        x_des, y_des = i_des // 3, i_des % 3
                        dx, dy = abs(x_state - x_des), abs(y_state - y_des)
                        d1, d2 = 1, math.sqrt(2)
                        custom_tiles += d1 * (dx + dy) + \
                            (d2 - 2 * d1) * min(dx, dy)
        return custom_tiles
    else:
        return 0


states_explored = 0
states_to_optimal_path = 0
success = False
optimal_path = []
heuristics = ["Zero", "Displaced", "Manhattan", "Custom"]
states = [set() for _ in range(4)]


def print_state(state):
    for i in range(9):
        if state[i] == 0:
            print("B", end=" ")
        else:
            print(state[i], end=" ")
        if i % 3 == 2:
            print()


def print_path(optimal_path):
    for i, state in enumerate(optimal_path):
        print("State", i + 1)
        print_state(state)


def A_Star(source_state, goal_state, heuristic):
    parent = {}
    open_list = []
    closed_list = set()
    states_exp = set()
    f = {}
    monotone_restriction = True

    open_list.append((0, tuple(source_state)))
    states_exp.add(tuple(source_state))
    f[tuple(source_state)] = 0

    while open_list:
        p = open_list.pop(0)
        state = list(p[1])
        state_cur = list(p[1])
        cur_h = h(state_cur, goal_state, heuristic)
        g = p[0] - cur_h

        if state == source_state:
            g = 0

        if tuple(state) in closed_list:
            pass
        else:
            pass

        # Convert list to tuple for adding to set
        closed_list.add(tuple(state))

        if state == goal_state:
            success = True
            curr_state = goal_state
            optimal_path = []
            while True:
                optimal_path.append(list(curr_state))
                if curr_state == source_state:
                    break
                curr_state = parent[tuple(curr_state)]
            states_to_optimal_path = len(optimal_path)
            optimal_path.reverse()
            break

        empty_cell = state.index(0)
        state_copy = list(state)

        # swap from up
        if empty_cell >= 3:
            state[empty_cell -
                  3], state[empty_cell] = state[empty_cell], state[empty_cell - 3]
            if tuple(state) not in closed_list:
                if tuple(state) in states_exp:
                    if f[tuple(state)] > g + 1 + h(state, goal_state, heuristic):
                        new_h = h(state, goal_state, heuristic)
                        if cur_h > 1 + new_h:
                            monotone_restriction = False
                        open_list.remove((f[tuple(state)], state))
                        f[tuple(state)] = g + 1 + \
                            h(state, goal_state, heuristic)
                        open_list.append((f[tuple(state)], state))
                        parent[tuple(state)] = state_copy
                else:
                    new_h = h(state, goal_state, heuristic)
                    if cur_h > 1 + new_h:
                        monotone_restriction = False
                    f[tuple(state)] = g + 1 + h(state, goal_state, heuristic)
                    open_list.append((f[tuple(state)], state))
                    states_exp.add(tuple(state))
                    parent[tuple(state)] = state_copy
            state[empty_cell -
                  3], state[empty_cell] = state[empty_cell], state[empty_cell - 3]

        # ... Repeat similar swaps for other directions ...

    states_explored = len(states_exp)
    if heuristic == "manhattan":
        states[2] = states_exp
    elif heuristic == "displaced":
        states[1] = states_exp
    elif heuristic == "custom":
        states[3] = states_exp
    else:
        states[0] = states_exp

    return monotone_restriction


failure = False


def search_result(source_state, goal_state, heuristic):
    global states_explored, success, optimal_path
    states_explored = 0
    success = False
    optimal_path = []

    start = time.time()
    monotone_restriction = A_Star(source_state, goal_state, heuristic)
    stop = time.time()
    duration = int((stop - start) * 1000)
    temp = "false"
    if monotone_restriction:
        temp = "true"

    if success:
        print("*********** Results for", heuristic, "heuristic ************")
        print("Success!!!")
        print("Source State:")
        print_state(source_state)
        print("Goal State:")
        print_state(goal_state)
        print("States Explored:", states_explored)
        print("Number of states to optimal path:", states_to_optimal_path)
        print("Optimal Path Cost:", states_to_optimal_path - 1)
        print("Time taken for execution:", duration, "milliseconds")
        print("Monotone Restriction:", temp)
    else:
        global failure
        failure = True
        print("*********** Results for", heuristic, "heuristic ************")
        print("Failure :(")
        print("Source State:")
        print_state(source_state)
        print("Goal State:")
        print_state(goal_state)
        print("States Explored before termination:", states_explored)
        print("Time taken for execution:", duration, "milliseconds")
    print()


def main():
    global source_state, goal_state
    source_state = generateRandomState()
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    search_result(source_state, goal_state, "Zero")
    search_result(source_state, goal_state, "Displaced")
    search_result(source_state, goal_state, "Manhattan")
    search_result(source_state, goal_state, "Custom")

    print("States comparisons for diff. heuristics:")
    if not failure:
        for i in range(4):
            for j in range(4):
                if i == j:
                    continue
                is_a_subset = states[i].issubset(states[j])
                temp = " is " if is_a_subset else " is not "
                print(heuristics[i] + temp + "a subset of " + heuristics[j])


if __name__ == "__main__":
    main()

#include <bits/stdc++.h>
#define int long long int
using namespace std;
using namespace std::chrono;
/// 0 to 8 tiles
/// 0 ==> B

vector<int> source_state;
vector<int> goal_state;
int inf = 1000000000;

vector<int> generateRandomState()
{ /// Function to generate a Random tuple of 0-8
    vector<int> state;
    for (int i = 0; i < 9; i++)
    {
        state.push_back(i);
    }
    mt19937 mt(time(nullptr)); /// mt19937 Random Number Generator
    for (int i = 8; i > 0; i--)
    {
        int index = mt() % (i + 1);
        swap(state[i], state[index]);
    }
    return state;
}

int h(vector<int> state, vector<int> des, string heuristic)
{
    if (heuristic == "manhattan")
    {
        int manhattan_dis = 0;
        for (int tile = 1; tile <= 8; tile++)
        {
            for (int i_state = 0; i_state <= 8; i_state++)
            {
                for (int i_des = 0; i_des <= 8; i_des++)
                {
                    /// calculating x and y coordinates for tiles in both states
                    if (state[i_state] == tile && des[i_des] == tile)
                    {
                        int x_state = i_state / 3;
                        int y_state = i_state % 3;
                        int x_des = i_des / 3;
                        int y_des = i_des % 3;
                        manhattan_dis += abs(x_state - x_des) + abs(y_state - y_des);
                    }
                }
            }
        }
        return manhattan_dis;
    }
    else if (heuristic == "displaced")
    {
        int displaced_tiles = 0;
        for (int i = 0; i <= 8; i++)
        {
            if (state[i] == 0)
            {
                continue;
            }
            if (state[i] != des[i])
            {
                displaced_tiles++;
            }
        }
        return displaced_tiles;
    }
    else if (heuristic == "custom")
    {
        int custom_tiles = 0;
        for (int tile = 1; tile <= 8; tile++)
        {
            for (int i_state = 0; i_state <= 8; i_state++)
            {
                for (int i_des = 0; i_des <= 8; i_des++)
                {
                    /// calculating x and y coordinates for tiles in both states
                    if (state[i_state] == tile && des[i_des] == tile)
                    {
                        int x_state = i_state / 3;
                        int y_state = i_state % 3;
                        int x_des = i_des / 3;
                        int y_des = i_des % 3;
                        int dx = abs(x_state - x_des);
                        int dy = abs(y_state - y_des);
                        double d1 = 1;
                        double d2 = sqrt(2);
                        custom_tiles += d1 * (dx + dy) + (d2 - 2 * d1) * min(dx, dy);
                    }
                }
            }
        }
        return custom_tiles;
    }
    else
    {
        return 0;
    }
}

int states_explored = 0;
int states_to_optimal_path = 0; /// distance
bool success = false;
vector<vector<int>> optimal_path;
void print_state(vector<int> state)
{

    for (int i = 0; i < 9; i++)
    {
        if (state[i] == 0)
        {
            cout << "B ";
        }
        else
        {
            cout << state[i] << " ";
        }
        if (i % 3 == 2)
        {
            cout << endl;
        }
    }
}

void print_path(vector<vector<int>> optimal_path)
{
    for (int i = 0; i < optimal_path.size(); i++)
    {
        cout << "State " << i + 1 << endl;
        print_state(optimal_path[i]);
    }
}

set<vector<int>> states[4];
string heuristics[] = {"Zero", "Displaced", "Manhattan", "Custom"};

bool A_Star(vector<int> source_state, vector<int> goal_state, string heuristic)
{
    map<vector<int>, vector<int>> parent;
    set<pair<int, vector<int>>> open_list; /// first element of pair is F, second is the state(vector)
    set<vector<int>> closed_list;
    set<vector<int>> states_exp;
    map<vector<int>, int> f;
    bool monotone_restriction = true;

    open_list.insert(make_pair(0, source_state));
    states_exp.insert(source_state);
    f[source_state] = 0;

    while (open_list.size())
    {
        pair<int, vector<int>> p = (*open_list.begin());
        vector<int> state = p.second;
        vector<int> state_cur = p.second;
        int cur_h = h(state_cur, goal_state, heuristic);
        int g = p.first - cur_h;

        if (state == source_state)
        {
            g = 0;
        }
        open_list.erase(p);

        if (closed_list.find(state) != closed_list.end())
        {
            /*if(f[state] > p.first ){
                f[state] = p.first;
            }*/
        }
        else
        {
            // f[state] = p.first;
        }

        closed_list.insert(state);

        if (state == goal_state)
        {
            success = true;
            vector<int> curr_state = goal_state;
            optimal_path = {};
            while (1)
            {
                optimal_path.push_back(curr_state);
                if (curr_state == source_state)
                {
                    break;
                }
                curr_state = parent[curr_state];
            }
            states_to_optimal_path = optimal_path.size();
            reverse(optimal_path.begin(), optimal_path.end());
            break;
        }

        int empty_cell = 0;
        for (int i = 0; i < 9; i++)
        {
            if (state[i] == 0)
            {
                empty_cell = i;
                break;
            }
        }
        vector<int> state_copy = state;
        // swap from up
        if (empty_cell >= 3)
        {
            swap(state[empty_cell - 3], state[empty_cell]);
            if (closed_list.find(state) == closed_list.end())
            {
                if (states_exp.find(state) != states_exp.end())
                {
                    if (f[state] > g + 1 + h(state, goal_state, heuristic))
                    {
                        int new_h = h(state, goal_state, heuristic);
                        if (cur_h > 1 + new_h)
                            monotone_restriction = false;
                        open_list.erase(make_pair(f[state], state));
                        f[state] = g + 1 + h(state, goal_state, heuristic);
                        open_list.insert(make_pair(f[state], state));
                        parent[state] = state_copy;
                    }
                }
                else
                {
                    int new_h = h(state, goal_state, heuristic);
                    if (cur_h > 1 + new_h)
                        monotone_restriction = false;
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    states_exp.insert(state);
                    parent[state] = state_copy;
                }
            }
            /*else{
                if(f[state] > g + 1 + h(state, goal_state, heuristic) ){
                    closed_list.erase(state);
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    parent[state] = state_copy;
                }
            }*/
            swap(state[empty_cell - 3], state[empty_cell]);
        }
        // swap from bottom
        if (empty_cell <= 5)
        {
            swap(state[empty_cell + 3], state[empty_cell]);
            if (closed_list.find(state) == closed_list.end())
            {
                if (states_exp.find(state) != states_exp.end())
                {
                    if (f[state] > g + 1 + h(state, goal_state, heuristic))
                    {
                        int new_h = h(state, goal_state, heuristic);
                        if (cur_h > 1 + new_h)
                            monotone_restriction = false;
                        open_list.erase(make_pair(f[state], state));
                        f[state] = g + 1 + h(state, goal_state, heuristic);
                        open_list.insert(make_pair(f[state], state));
                        parent[state] = state_copy;
                    }
                }
                else
                {
                    int new_h = h(state, goal_state, heuristic);
                    if (cur_h > 1 + new_h)
                        monotone_restriction = false;
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    states_exp.insert(state);
                    parent[state] = state_copy;
                }
            }
            /*else{
                if(f[state] > g + 1 + h(state, goal_state, heuristic) ){
                    closed_list.erase(state);
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    parent[state] = state_copy;
                }
            }*/
            swap(state[empty_cell + 3], state[empty_cell]);
        }
        // swap from left
        if (empty_cell % 3 > 0)
        {
            swap(state[empty_cell - 1], state[empty_cell]);
            if (closed_list.find(state) == closed_list.end())
            {
                if (states_exp.find(state) != states_exp.end())
                {
                    if (f[state] > g + 1 + h(state, goal_state, heuristic))
                    {
                        int new_h = h(state, goal_state, heuristic);
                        if (cur_h > 1 + new_h)
                            monotone_restriction = false;
                        open_list.erase(make_pair(f[state], state));
                        f[state] = g + 1 + h(state, goal_state, heuristic);
                        open_list.insert(make_pair(f[state], state));
                        parent[state] = state_copy;
                    }
                }
                else
                {
                    int new_h = h(state, goal_state, heuristic);
                    if (cur_h > 1 + new_h)
                        monotone_restriction = false;
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    states_exp.insert(state);
                    parent[state] = state_copy;
                }
            }
            /*else{
                if(f[state] > g + 1 + h(state, goal_state, heuristic) ){
                    closed_list.erase(state);
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    parent[state] = state_copy;
                }
            }*/
            swap(state[empty_cell - 1], state[empty_cell]);
        }
        // swap from right
        if (empty_cell % 3 < 2)
        {
            swap(state[empty_cell + 1], state[empty_cell]);
            if (closed_list.find(state) == closed_list.end())
            {
                if (states_exp.find(state) != states_exp.end())
                {
                    if (f[state] > g + 1 + h(state, goal_state, heuristic))
                    {
                        int new_h = h(state, goal_state, heuristic);
                        if (cur_h > 1 + new_h)
                            monotone_restriction = false;
                        open_list.erase(make_pair(f[state], state));
                        f[state] = g + 1 + h(state, goal_state, heuristic);
                        open_list.insert(make_pair(f[state], state));
                        parent[state] = state_copy;
                    }
                }
                else
                {
                    int new_h = h(state, goal_state, heuristic);
                    if (cur_h > 1 + new_h)
                        monotone_restriction = false;
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    states_exp.insert(state);
                    parent[state] = state_copy;
                }
            }
            /*else{
                if(f[state] > g + 1 + h(state, goal_state, heuristic) ){
                    closed_list.erase(state);
                    f[state] = g + 1 + h(state, goal_state, heuristic);
                    open_list.insert(make_pair(f[state], state));
                    parent[state] = state_copy;
                }
            }*/
            swap(state[empty_cell + 1], state[empty_cell]);
        }
    }
    states_explored = states_exp.size();
    if (heuristic == "manhattan")
        states[2] = states_exp;
    else if (heuristic == "displaced")
        states[1] = states_exp;
    else if (heuristic == "custom")
        states[3] = states_exp;
    else
        states[0] = states_exp;

    return monotone_restriction;
}

bool failure = false;

void search_result(vector<int> source_state, vector<int> goal_state, string heuristic)
{
    states_explored = 0;
    success = false;
    optimal_path.clear();

    auto start = high_resolution_clock::now();
    bool monotone_restriction = A_Star(source_state, goal_state, heuristic);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    string temp = "false";
    if (monotone_restriction)
        temp = "true";

    if (success)
    {
        cout << "*********** Results for " << heuristic << " heuristic ************" << endl;
        cout << "Success!!!" << endl;
        cout << "Source State: " << endl;
        print_state(source_state);
        cout << "Goal State: " << endl;
        print_state(goal_state);
        cout << "States Explored: " << states_explored << endl;
        cout << "Number of states to optimal path: " << states_to_optimal_path << endl;
        cout << "Optimal Path Cost: " << states_to_optimal_path - 1 << endl;
        // cout<<"Optimal Path: "<<endl;
        // print_path(optimal_path);
        cout << "Time taken for execution " << duration.count() << " milliseconds" << endl;
        cout << "Monotone Restriction: " << temp << endl;
    }
    else
    {
        failure = true;
        cout << "*********** Results for " << heuristic << " heuristic ************" << endl;
        cout << "Failure :(" << endl;
        cout << "Source State: " << endl;
        print_state(source_state);
        cout << "Goal State: " << endl;
        print_state(goal_state);
        cout << "States Explored before termination: " << states_explored << endl;
        cout << "Time taken for execution " << duration.count() << " milliseconds" << endl;
    }
    cout << endl;
}

signed main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    // source_state = generateRandomState();
    // source_state = {2, 3, 6, 1, 4, 0, 7, 5, 8};
    source_state = {6, 1, 7, 2, 0, 8, 3, 4, 5};
    // source_state = {1,2,3,4,5,6,7,0,8};
    goal_state = {1, 2, 3, 4, 5, 6, 7, 8, 0};

    search_result(source_state, goal_state, "zero");
    search_result(source_state, goal_state, "displaced");
    search_result(source_state, goal_state, "manhattan");
    search_result(source_state, goal_state, "custom");

    cout << "States comparisons for diff. heuristics:\n";

    if (!failure)
    {
        for (int i = 0; i < 4; i++)
        {
            for (int j = 0; j < 4; j++)
            {
                if (i == j)
                    continue;
                bool is_a_subset = true;
                for (auto x : states[i])
                    if (states[j].find(x) == states[j].end())
                    {
                        is_a_subset = false;
                        break;
                    }
                string temp = " is ";
                if (!is_a_subset)
                    temp += "not ";
                cout << heuristics[i] << temp << "a subset of " << heuristics[j] << "\n";
            }
        }
    }
}
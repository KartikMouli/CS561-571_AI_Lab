/*

CS571 : Assignment 2
Group Members Roll No.s : 2001CS35,2001CS56,2001CS70

*/

// including required libraries
#include <bits/stdc++.h>
using namespace std;

// using chrono for time
using namespace std::chrono;

// define ll as long long
#define ll long long

// define a vector to store source and goal state
vector<ll> source_state;
vector<ll> goal_state;

ll states_explored = 0;        // states explored
ll states_to_optimal_path = 0; // distance

vector<vector<ll>> optimal_path; // stores optimal path to reach target state

// declare states
set<vector<ll>> states[4];
string heuristics[] = {"Zero", "Displaced", "Manhattan", "Euclidean"};

// define booleans
bool failure = false;
bool success = false;

// function to generate random grid
vector<ll> generateRandomState()
{
    // vector to store current state
    vector<ll> state = {0, 1, 2, 3, 4, 5, 6, 7, 8};

    mt19937 mt(time(nullptr)); /// mt19937 Random Number Generator
    // generate random state
    for (ll i = 8; i > 0; i--)
    {
        ll index = mt() % (i + 1);
        swap(state[i], state[index]);
    }
    return state;
}

// 0-> zero     (h1)
// 1->displaced (h2)
// 2->manhattan (h3)
// 3->euclidean (h4)
ll h(vector<ll> state, vector<ll> des, ll heuristic)
{
    // using switch for heuristic
    switch (heuristic)
    {
    case 0:
        // h(0)=0
        return 0;
        break;
    case 1:
    {
        // calculating displaced tiles  h(1)
        ll displaced_tiles = 0;
        for (ll i = 0; i <= 8; i++)
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
    break;
    case 2:
    {
        // calculating manhattan distance h(2)
        ll manhattan_dis = 0;
        for (ll tile = 1; tile <= 8; tile++)
        {
            for (ll i_state = 0; i_state <= 8; i_state++)
            {
                for (ll i_des = 0; i_des <= 8; i_des++)
                {
                    /// calculating x and y coordinates for tiles in both states
                    if (state[i_state] == tile && des[i_des] == tile)
                    {
                        // calculate co-ordinates x and y
                        ll x_state = i_state / 3;
                        ll y_state = i_state % 3;
                        ll x_des = i_des / 3;
                        ll y_des = i_des % 3;
                        manhattan_dis += abs(x_state - x_des) + abs(y_state - y_des);
                    }
                }
            }
        }
        return manhattan_dis;
    }
    break;
    case 3:
    {
        // calculating euclidean distance h(3)
        ll custom_tiles = 0;
        for (ll tile = 1; tile <= 8; tile++)
        {
            for (ll i_state = 0; i_state <= 8; i_state++)
            {
                for (ll i_des = 0; i_des <= 8; i_des++)
                {
                    /// calculating x and y coordinates for tiles in both states
                    if (state[i_state] == tile && des[i_des] == tile)
                    {
                        // calculate co-ordinates x and y
                        ll x_state = i_state / 3;
                        ll y_state = i_state % 3;
                        ll x_des = i_des / 3;
                        ll y_des = i_des % 3;
                        ll dx = abs(x_state - x_des);
                        ll dy = abs(y_state - y_des);
                        double d1 = 1;
                        double d2 = sqrt(2);
                        // euclidean formula
                        custom_tiles += d1 * (dx + dy) + (d2 - 2 * d1) * min(dx, dy);
                    }
                }
            }
        }
        return custom_tiles;
    }
    break;
    default:
        return -1;
        break;
    }
}

// function to print state
void print_state(vector<ll> state)
{

    for (ll i = 0; i < 9; i++)
    {
        if (state[i] == 0)
            cout << "B ";
        else
            cout << state[i] << " ";
        if (i % 3 == 2)
            cout << '\n';
    }
}

// function to print optimal path
void print_path(vector<vector<ll>> optimal_path)
{
    for (ll i = 0; i < optimal_path.size(); i++)
    {
        cout << "State " << i + 1 << endl;
        print_state(optimal_path[i]);
        cout << '\n';
    }
}

// function to update state
void updateState(set<vector<ll>> &closed_list, set<vector<ll>> &states_exp, set<pair<ll, vector<ll>>> &open_list, map<vector<ll>, ll> &f, ll g, map<vector<ll>, vector<ll>> &parent, vector<ll> state, vector<ll> state_copy, vector<ll> goal_state, ll heuristic, ll cur_h, bool monotone_restriction)
{
    // if current state is not in closed list
    if (closed_list.find(state) == closed_list.end())
    {
        // if current state is already explored
        if (states_exp.find(state) != states_exp.end())
        {
            // if f(n) > cost_of_path(n) + 1 + h(n')
            if (f[state] > g + 1 + h(state, goal_state, heuristic))
            {
                // calculating new heuristic
                ll new_h = h(state, goal_state, heuristic);
                // check monotone restriction
                if (cur_h > 1 + new_h)
                    monotone_restriction = false;
                // remove the state from open list and insert new state with updated f(n)
                open_list.erase(make_pair(f[state], state));
                f[state] = g + 1 + h(state, goal_state, heuristic);
                open_list.insert(make_pair(f[state], state));
                parent[state] = state_copy;
            }
        }
        else
        {
            // calculating new heuristic
            ll new_h = h(state, goal_state, heuristic);
            // check monotone restriction
            if (cur_h > 1 + new_h)
                monotone_restriction = false;
            f[state] = g + 1 + h(state, goal_state, heuristic);
            // insert new state with updated f(n)
            open_list.insert(make_pair(f[state], state));
            states_exp.insert(state);
            parent[state] = state_copy;
        }
    }
}

bool A_Star(vector<ll> source_state, vector<ll> goal_state, ll heuristic)
{
    // defining required data structures
    map<vector<ll>, vector<ll>> parent;
    set<pair<ll, vector<ll>>> open_list; /// first element of pair is F, second is the state(vector)
    set<vector<ll>> closed_list;
    set<vector<ll>> states_exp;
    map<vector<ll>, ll> f;
    bool monotone_restriction = true;

    // insert source state int open list and explored states
    open_list.insert(make_pair(0, source_state));
    states_exp.insert(source_state);

    // store f(n)
    f[source_state] = 0;

    // exploring all states in open list
    while (open_list.size())
    {
        pair<ll, vector<ll>> p = (*open_list.begin());
        vector<ll> state = p.second;
        vector<ll> state_cur = p.second;
        ll cur_h = h(state_cur, goal_state, heuristic);
        ll g = p.first - cur_h;

        if (state == source_state)
        {
            g = 0;
        }
        open_list.erase(p);

        closed_list.insert(state);

        // if we rech the target state,store the path and  break the loop
        if (state == goal_state)
        {
            success = true;
            vector<ll> curr_state = goal_state;
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

        // find empty cell in state
        ll empty_cell = 0;
        for (ll i = 0; i < 9; i++)
        {
            if (state[i] == 0)
            {
                empty_cell = i;
                break;
            }
        }

        vector<ll> state_copy = state;
        // swap from up
        if (empty_cell >= 3)
        {
            swap(state[empty_cell - 3], state[empty_cell]);
            updateState(closed_list, states_exp, open_list, f, g, parent, state, state_copy, goal_state, heuristic, cur_h, monotone_restriction);
            swap(state[empty_cell - 3], state[empty_cell]);
        }
        // swap from down
        if (empty_cell <= 5)
        {
            swap(state[empty_cell + 3], state[empty_cell]);
            updateState(closed_list, states_exp, open_list, f, g, parent, state, state_copy, goal_state, heuristic, cur_h, monotone_restriction);
            swap(state[empty_cell + 3], state[empty_cell]);
        }
        // swap from left
        if (empty_cell % 3 > 0)
        {
            swap(state[empty_cell - 1], state[empty_cell]);
            updateState(closed_list, states_exp, open_list, f, g, parent, state, state_copy, goal_state, heuristic, cur_h, monotone_restriction);
            swap(state[empty_cell - 1], state[empty_cell]);
        }
        // swap from right
        if (empty_cell % 3 < 2)
        {
            swap(state[empty_cell + 1], state[empty_cell]);
            updateState(closed_list, states_exp, open_list, f, g, parent, state, state_copy, goal_state, heuristic, cur_h, monotone_restriction);
            swap(state[empty_cell + 1], state[empty_cell]);
        }
    }
    states_explored = states_exp.size();

    // switch case for heuristic store explored state in mapped states
    switch (heuristic)
    {
    case 0:
        states[0] = states_exp;
        break;
    case 1:
        states[1] = states_exp;
        break;
    case 2:
        states[2] = states_exp;
        break;
    case 3:
        states[3] = states_exp;
        break;
    default:
        break;
    }

    return monotone_restriction;
}

// function to print stored results
void search_result(vector<ll> source_state, vector<ll> goal_state, ll heuristic)
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
        cout << "----------- Results for "
             << "h(" << heuristic + 1 << ") " << heuristics[heuristic] << " Heuristic -----------" << endl;
        cout << "Operation Successful!" << endl;
        cout << "Initial State: " << endl;
        print_state(source_state);
        cout << "Target State: " << endl;
        print_state(goal_state);
        cout << "States Explored: " << states_explored << endl;
        cout << "Number of States to Optimal Path: " << states_to_optimal_path << endl;
        cout << "Optimal Path Cost: " << states_to_optimal_path - 1 << endl;
        cout << "Optimal Path: " << endl;
        print_path(optimal_path);
        cout << "Execution Duration: " << duration.count() << " milliseconds" << endl;
        cout << "Monotonic Constraint: " << temp << endl;
    }
    else
    {
        failure = true;
        cout << "----------- Result for "
             << "h(" << heuristic + 1 << ") " << heuristics[heuristic] << " Heuristic -----------" << endl;
        cout << "Operation Unsuccessful :(" << endl;
        cout << "Initial State: " << endl;
        print_state(source_state);
        cout << "Target State: " << endl;
        print_state(goal_state);
        cout << "States Explored prior to Termination: " << states_explored << endl;
        cout << "Execution Duration: " << duration.count() << " milliseconds" << endl;
    }
    cout << endl;
}

signed main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    cerr << "Code is executing...\nplease wait :)\n";

    // Open the file for writing
    std::ofstream outputFile("output.txt");

    // Save the current cout buffer
    std::streambuf *coutBuffer = std::cout.rdbuf();

    // Redirect cout to the file
    std::cout.rdbuf(outputFile.rdbuf());

    // generate random source state
    // source_state = generateRandomState();
    // source_state = {2, 3, 6, 1, 4, 0, 7, 5, 8};
    // source_state = {6, 1, 7, 2, 0, 8, 3, 4, 5};
    source_state = {1, 2, 3, 4, 5, 6, 0, 7, 8};
    // source_state = {1, 3, 6, 0, 4, 7, 5, 8, 2};

    // source_state = {1, 2, 3, 4, 5, 6, 7, 0, 8};
    goal_state = {1, 2, 3, 4, 5, 6, 7, 8, 0};

    // if we hit success print desired results
    for (ll i = 0; i != 4; i++)
    {
        search_result(source_state, goal_state, i);
    }

    // States comparison for diff. heuristics
    if (!failure)
    {
        cout << "States comparisons for diff. heuristics:\n\n";
        for (ll i = 0; i < 4; i++)
        {
            for (ll j = 0; j < 4; j++)
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

    // Restore the original cout buffer
    std::cout.rdbuf(coutBuffer);

    // Close the file
    outputFile.close();

    cerr << "Execution Completed..!!\n";

    return 0;
}

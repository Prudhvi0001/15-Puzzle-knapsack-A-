# A1

## Part 1: The Luddy puzzle

#### Initial State:

4X4 Board Configuration with numbers from 0-15(where '0' denotes an empty tile) which is Given as input.

#### Goal State:

Canonical Configuration of the board with numbers 1-15 and 0 at the bottom right tile arranged in order.

|  1    |  2    |   3   |    4  |
| ---- | ---- | :--: | ---- |
|   5   |   6   |   7   |    8  |
|    9  |   10   |  11   |   12   |
|   13   |   14   |   15   |   0   |

#### State Space:

State Space consists of all the possible board configurations which result from a valid move.
Each variant has different State Spaces depending on their moves.

#### Successor Function:

###### Original:

The Successor function consists of all possible moves for the empty tile to move one tile in any all four directions within the table constraints. such as (L,R,U,D)

|       |  ⬆   |      |      |
| :---:| ---- | :---: | :---: 
|  ⬅   |  0   |  ➡  |      |
|       |  ⬇   |      |      |
|       |      |      |      |

##### Circular:

The Successor function consists of all possible moves for the empty tile to move in all of its original directions and when the empty tile is at edges it can swap itself to the opposite side. which are denoted as Right Circular Rotation, Up Circular Rotation, Left Circular Rotation, Down Circular Rotation(CR,CL,CU,CD)

|       |      |       | **↰** |
| :---: | ---- | :---: | :---: |
|       |      |       |       |
|       |      |       | **⬆** |
| **↩** |      | **⬅** |   0   |

##### Luddy:

The Successor function consists of all possible moves for the empty tile to move in L shape with (2,1)(1,2) combinations in different directions. which are encoded in the program as (A,B,C,D,E,F,G,H)


|       | **D** |       |  C   |
| :---: | :---: | :---: | :--: |
| **H** |       |       |      |
|       |       | **0** |      |
| **F** |       |       |      |


#### Heuristic Function:

Manhattan distance : Is the sum of Manhattan distances of every tile from its Given state to goal state except the empty tile.

|      |      |      |      |
| ---- | ---- | :--: | ---- |
|      |      |      |      |
|      |      |  1   |      |
|      |      |      |      |

|  14️⃣  | ◀ 3️⃣  |  🔼2️⃣  |      |
| :--:  | :--:   | :--:    | ---- |
|       |        |  🔼1️⃣  |      |
|       |        |  1      |      |
|       |        |         |      |

If the variant is original, we directly sum up all the manhattan distances .
if the variant is either circular or luddy ... we do sum up all the manhattan distances , but before than we normalize the distances .
We normalized the distances which were greater than or equal to 3 because in these two cases we can move upto 3 places at a time i.e. in circular we can shift a tile from one end to the other end,so if a tile is 3 units away from its goal state, it can reach it in one move,similarly for  luddy moves we can shift 3 places in a single move.So, the number of steps to its goal state can be normalized to 1.

|  7   |      |      |      |
| :--: | :--: | :--: | :--: |
|      |      |  0   |      |
|      |      |      |      |
|      |      |      |      |

|  0   |  1️⃣   |  2️⃣   |      |
| :--: | :--: | :--: | ---- |
|      |       |  3️⃣7  |      |
|      |       |        |      |
|      |       |        |      |


This heuristic is admissable and consistent .hence we used search algorithm 3. And also we couldn't find any case where it fails.
But, it is taking lot of time for boardn , we dint find boardn solvable .

We also tried Heuristic functions:

> Misplaced Tiles 
>
> Manhattan/3 - Misplaced Tiles - this was admissable and consistent but it's performance was slow
>
> Manhattan of only two rows - performance was slow
>
> Manhattan of even numbers in the table - performance was slow

#### A* Implementation:

1. Depending on the Variant the Board the moves list is considered 

2. Check if the Initial Board is Goal state.?

3.We ahve used  Priority Queue to store the fowllowing (a,(b,c))

   > a is sum of  estimated cost (which is nothing but heuristic distance) + cumulative cost (which is nothing but length of tree it has traveled so far)
   >
   > b is cumulative cost (which is nothing but length of tree it has traveled so far)
   >
   > c is the Successor board for the given board

> 

4. All the Successor for the initial board are taken and compared with Goal state if True then it returns the path of the successor.

5. If not it will compute the Heuristic value, Cumulative distance value to the successor and store in the fringe.

6. For the next iteration the priority queue returns board with least estimated cost to the goal state from the fringe. And this process Continues till the Goal state is reached.


Note : Since we are not calculating the permutation invesrions, if a given board is unsolvable ,this might take really long time trying to find explore the entire search space for a given variant .

   #### 

## Part 2: The Road Network

We have built a road network which basically is a group of city objects which contain data about city,state,latitude,longitude, each of these cities are  mapped to the route objects ,which contain data such as  the city you can reach from this city,distance between them,speed,highway .We have also generated new cities and mapped to their corrsponding route data,which weren't provided in the city data ,but present in road_segments file and assigned default latitude and longitude values as -1 .

#### Initial State:
Given a graph/road_network we have start_city as the initial state .

#### Goal State:
Given a a graph/road_network , when we reach from a start_city to the end_city , end_city is our goal state.

#### State Space:
State Space for any given cost_function is all the neighbouring cities one can reach from a given city.

#### Successor Function:
The successor function returns all the neighbouring cities which can be reached from a given city ,but not the cities which have already visited, since we are using search algorithm 3.

#### Heuristic Function:

##### Cost Function : Distance 
 We are using the haversine formula to calculate distance from a given city to the end city .This formula gives us the distance in miles between these cities.We do have a problem here due to insuffient latitude and longitude data .We have overcome this problem by calculating weighted average of distance and corodinate data from the neighbouring cities.But, still there is some serious problem if even the neighbouring cities do not have corodinate data, we tried to overcome this by recursively finding out corodinates from neighbours of neighbours upto a depth of 5, if it fails to find any corodinate even after reaching out to the depth of 5 for a neighbouring city, then we are returning the average latitudes and longitudes for the whole graph .</br>
     Due to this ,there are instances where the heuristic might sometimes overestimate or under estimate because the actual latitude and longitude might be bit lower than or higher than the average values.</br>
     For example, for cases with cities in Quebec where all of the cities do not have latitude and longitude values ,if we have to traverse to any city in Quebec to any other city in Quebec .. the heuristic is trapped in taking average coordinates ,which will result in a poor performance.</br>
     And for cases like where start_city : city1 and end_city : city 2 , you might get an optimal path but, if the start_city : city2 and end_city : city1 .. you might get a slight variation because of the distance caculation.
     We have also tried taking state averages , but that did not improve any performance and we have also tried implementing search algorithm 2 where we were considering the visited cities as successors too , and having our heuristic 0 if there wasn't sufficient coordinate data .But, it is increasing the state space and running way too slow .</br>
     We set this heuristic cost + cummulative cost till that city as priority ,so that the least distance path would be considered first for exploring.This heuristic is admissable and consistent for all the cities with sufficient coordinate data.</br>

##### Cost Function : Segments 
 We have used the distance heuristic itself to find the least distance but ,while inserting the priority we are adding 1 in order to note that we have crossed one segment and the priority queue will give us the least legmented path each time for exploring.This heuristic is admissable and consistent for all the cities with sufficient coordinate data.
    
##### Cost Function : Time 
 We have used the distance heuristic itself to find the distance and then for a given city, we are finding out the maximum speed along all the routes from that city to its neightbouring city and then estimating time by  distance/speed which would give an estimate along that path ,This would suggest that ..given a city ,its distance to end_city .. if we are mainataining the maximum speed , we can reach the end city in a certain time. This heuristic is admissable and consistent for all the cities with sufficient coordinate data.
 
 ##### Cost Function : mpg 
 We have used the formula given in the problem statement for calculating the heuristic, but here for a given city we are only considering the maximum speed among all the routes from this city to calculate the mpg because the mpg is directly proportional to the velocity .So, maximum the velocity , maximum is the mpg, maximum is the mpg, less is the consumption of the fuel.</br>
    Here, we are inserting the negative values of mpg in the priority queue, because , higher the value of mpg , lower will be its negative value, lower the value, higher will be the priority in the queue and will be able to explore that city first.
    


#### A* Implementation:

1. All neighbouring cities for a given city are the successors , provided they weren't visited before. 

2. Check if the city is is Goal state.?

3.We have used  Priority Queue to store the fowllowing (a,(b,c))

   > a is sum of  estimated cost (which is nothing but heuristic distance/time/mpg) + cumulative cost (segments/road_distance/time/mpg)
   >
   > b is cumulative cost (segments/road_distance/time/mp)
   >
   > c is the Successor city

4.If the successor is not the goal state, will compute the Heuristic value, Cumulative cost value to the successor and store in the fringe.

5. For the next iteration the priority queue returns city with least estimated cost to the goal state from the fringe. And this process Continues till the Goal state is reached.

   ####   

Problem -3 
 
We have used 0/1 knapsack branch and bound technique to solve this problem.
(https://www.youtube.com/watch?v=R6BQ3gBrfjQ)
We have referred to this video to improve our understanding about branch and bound.


                                                [A,B,C,D,E,F]
                                               /            \
                                              /              \
                                         1   /                \  0
                                            /                  \
                                        [B,C,D,E,F]        [B,C,D,E,F] 
                          Skill = A's skill cost              0
                   Rem_Budget = Total_Budget -A'cost          0
                         /      \                          /        \ 
                   1    /        \ 0                   1  /          \  0
                       /          \                      /            \
                    [C,D,E,F]    [B,C,D,E,F]    [C,D,E,F]     [B,C,D,E,F]
                 A+C skill cost    A's cost    B's skill cost          0
             Remaining-C's cost  Total - A's cost    Total_budget -B'scost     0
 

We have initially sorted the people according to their skill/rate ratio in an decreasing order and we have used 0/1 knap sack branch and bound technique to solve the problem.</br></br>
Initially we will have the list of sorted people.Then we have two states at each level , Either we pick the first first person from the list or the do not pick that person from the list . After choosing A we have completed(1,A) state and reached (-1,B)   and without choosing A we have completed(0,A) and reached (-1,B) state. Where 1 indicates A has been selected , 0 indicates A has not been selected.
What might be confusing in the code is -1 level . This is an intermediate level ,which has been created for programming convenience, it only states we have to look for people in the sorted list from B .</br>
The most important part of this technique is upper bound. We calculate the upperbound which is the maximum skill can be obtained along each path, basically each path is a permutation , so we keep track of the upper bound at each node and store a negative value of the upper bound in the priority queue, which helps us in retrieving the highest upper bound state first .</br></br>

So, if we finish exhausting the whole list, we end up with one permutation,it's total skill cost and total budget , we then store this team as max_team if it has maximum skill and the total budget is below or equal to the given budget, initially max_skill is 0.
Once we have this max_skill value.. we continue to explore other nodes for better skill , if any successor has an upperbound less than the already obtained max_skill value we will discard those nodes,thus minimising our search space.We continue to constantly cauculate the upper bounds and comapre with the maximum skill value , if a successor state has more skill value ,but its budget is more than the given budget,even then we discard those nodes.
We continue to do this untill we find the team with the maximum skill.
 
Initial State:
Assemble the robots in the decreasing order of their skill/rate ratio.
None of the robots have been choosen.
 
Goal State:
We achieve the goal state when we have exhausted the budget , where we can no longer assign a robot .Assemble a skilled team such that we have only whole robots, and our total cost is less than or equal to the budget and we have maximised the skill.
 
States & Successor Function :
While we are iterating until the goal is reached, our successor function returns a group of robots within the given budget constraint.Each time we will have two successors for a given state which is a successor with choosing the first robot in a given list and a successor without choosing the first robot in  agiven list.We add the estimated skill cost + cummulative skill cost till we have picked the robot as our priority.As mentioned earlier we store this estimated cost as a negative number to ensure it has higher priority.
 
Cost Function:
We compute the best skill possible on picking up a robot , and this is constrained by the budget we have .

#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [ Naga Anjaneyulu - nakopa , Ruthvik parvataneni -rparvat,Prudhvi Vajja - pvajja ]
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import sys

MOVES = { "original" :{ "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0)} ,
          "circular" : { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0),"CR": (0, 3), "CL": (0, -3), "CD": (-3, 0), "CU": (3,0) },
          "luddy" : {"A":(2,1), "B":(2,-1) , "C" :(-2,1) , "D":(-2,-1),"E":(1,2) ,"F":(1,-2) ,"G":(-1,2) , "H":(-1,-2)}}

def get_moves(state,variant):
     return MOVES[variant].items()

        
def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row,col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):

    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):

    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors(state,variant,path):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [succ for succ in [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in get_moves(state,variant) if valid_index(empty_row+i, empty_col+j) ] \
    if succ[0] not in path.keys() ]
    return [succ for succ in [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in get_moves(state,variant) if valid_index(empty_row+i, empty_col+j) ] \
    if succ[0] not in path.keys() ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
# compute heuristic cost
def compute_heuristic_cost(initial_board,variant,move):
    state = list(initial_board)
    state.remove(0)
    state = sorted(state)
    state.append(0)
 
    dist_list = [int((abs(i-j))/4) + int((abs(i-j))%4) for i in range(0,len(state)) for j in range(0,len(initial_board)) \
                          if state[i] == initial_board[j] and initial_board[j] != 0 ]
    man_dist =0
    if variant == "original":
        man_dist = sum(dist_list)
    else :
        for value in dist_list:
            if value >=3:
                man_dist += value/3
            else:
                man_dist += value

    return man_dist 
    
    
# The solver! - using BFS right now
def solve(initial_board,variant):
    
    fringe = PriorityQueue()
    est_cost = compute_heuristic_cost(initial_board,variant,"")
    cumm_cost =0
    path_dict = {}
    path_dict[initial_board] = ['']
    fringe.put((est_cost +cumm_cost,(cumm_cost,initial_board)))
    while not fringe.empty():
        (est_cost,(cost,state)) = fringe.get()
        if is_goal(state):
                return path_dict[state]
        for (succ, move) in successors(state,variant,path_dict):
            if is_goal(succ):
                path_dict[succ] = path_dict[state] + [move]
                return path_dict[succ]
            est_cost = compute_heuristic_cost(succ,variant,move)
            fringe.put((est_cost +cost+1, (cost+1,succ)))
            path_dict[succ] = path_dict[state] + [move]
    return None

if __name__ == "__main__":
# test cases
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
    variant = sys.argv[2]
#    if( variant != "original"):
#        raise(Exception("Error: only 'original' puzzle currently supported -- you need to implement the other two!"))

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state),variant)
    print("Solution found in " + str(len(''.join(route).replace("C",""))) + " moves:" + "\n" + ''.join(route).replace("C",""))


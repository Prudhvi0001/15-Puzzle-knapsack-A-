#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [ Naga Anjaneyulu - nakopa , Ruthvik parvataneni -rparvat,Prudhvi Vajja - pvajja ]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
from queue import PriorityQueue

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
        
            people[l[0]] = [ float(i) for i in l[1:] ] 
            
    return people

def successors(team,sorted_list,cumm_skill,total_budget,budget):
    rem_budget = total_budget - budget
    recently_added = team[len(team)-1]
    flag = recently_added[0]
    if flag == -1:
        team.pop()
    recent_index = sorted_list.index(recently_added[1])
    succ_list = []
    
    if( recent_index < len(sorted_list) and (flag == 1 or flag == -1) ):
        skill = compute_skill(recent_index ,sorted_list, rem_budget)
        if(skill > 0 and recent_index + 1 < len(sorted_list)):
            if flag == 1:
                 succ_list.append(([(-1,sorted_list[recent_index +1])],
                                    sorted_list[recent_index][1][1] + budget ,cumm_skill + skill,
                                   cumm_skill +  sorted_list[recent_index][1][0] ))
            elif flag == -1:
                succ_list.append(([ (1,sorted_list[recent_index]) , 
                                 (-1,sorted_list[recent_index +1])],
                                    sorted_list[recent_index][1][1] + budget ,cumm_skill + skill,
                                   cumm_skill +  sorted_list[recent_index][1][0] ))
                
        elif(skill > 0 and recent_index < len(sorted_list) and flag != 1):
            succ_list.append(([(1,sorted_list[recent_index])],
                                    sorted_list[recent_index][1][1] + budget ,cumm_skill + skill,
                                    cumm_skill +  sorted_list[recent_index][1][0]))
            
    if( recent_index + 1 < len(sorted_list) and (flag == 0 or flag == -1)):  
        skill = compute_skill(recent_index + 1 ,sorted_list, rem_budget)
        if(skill > 0 ):
            succ_list.append(([(0,sorted_list[recent_index ]),(-1,sorted_list[recent_index +1])],
                                     budget ,cumm_skill + skill,cumm_skill))
       
            
#          if(skill > 0 and recent_index + 2 < len(sorted_list)):
              
#             succ_list.append(([ (1,sorted_list[recent_index +1]) , 
#                                 (-1,sorted_list[recent_index +2])],
#                                     budget ,cumm_skill + skill))
#          elif(skill > 0 and recent_index +2 >= len(sorted_list)):
#            succ_list.append(([(0,sorted_list[recent_index + 1])],
#                                     budget ,cumm_skill + skill))
    return succ_list
    


def compute_skill(index,sorted_list,budget):
    total_skill = 0
    for (person, (skill, cost)) in sorted_list[index :]:
        if cost < budget and budget >= 0:
            total_skill += skill
            budget -= cost
        
    return total_skill
        

# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted. It exactly exhausts the budget
#  by adding a fraction of the last person.
#
def approx_solve(people, total_budget):
    sorted_list = sorted(people.items(), key=lambda x: x[1][1] / x[1][0])
    fringe = PriorityQueue()
    skill_1= compute_skill(0,sorted_list,total_budget)
    fringe.put((-float(skill_1),([(-1,sorted_list[0])] ,0,0)))
    max_skill =0
    max_team = ()
    max_budget = 0
    while not fringe.empty():
        (upper_bound,(team,skill,budget)) = fringe.get()
        succ_list = successors(team,sorted_list,skill,total_budget, budget)
        if len(succ_list) == 0 and budget <=total_budget:
            if skill > max_skill:
                max_skill,max_team,max_budget =  skill,team,budget
        else:
            for (succ,succ_budget,est_skill,act_skill) in succ_list:
               if(est_skill >= max_skill ) and succ_budget <= total_budget:
                   fringe.put((-float(est_skill) , ( team + succ, act_skill, succ_budget)))
                       
                
                
    return max_skill,max_team,max_budget
        

if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    max_skill,solution,max_budget = approx_solve(people, budget)
    solution =  [  (member[1][0],1)   for member in solution if member[0] == 1  ]
    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(solution), sum(people[p][1]*f for p,f in solution), sum(people[p][0]*f for p,f in solution)))

    for s in solution:
        print("%s %f" % s)


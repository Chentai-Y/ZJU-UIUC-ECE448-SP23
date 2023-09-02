# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    frontier = []
    frontier.append([maze.getStart()])
    explored = set()
    while frontier:
        now_path = frontier[0]
        del frontier[0]
        now_row, now_col = now_path[-1]
        if (now_row, now_col) in explored:
            continue     
        else:  
            explored.add((now_row, now_col))

        if maze.isObjective(now_row, now_col):
            return now_path, len(explored)
        else:
            for neighbors in maze.getNeighbors(now_row, now_col):
                if neighbors not in explored:
                    frontier.append(now_path + [neighbors])
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    frontier = []
    frontier.append([maze.getStart()])
    explored = set()
    while frontier:
        now_path = frontier[-1]
        del frontier[-1]
        now_row, now_col = now_path[-1]
        if (now_row, now_col) in explored:
            continue     
        else:  
            explored.add((now_row, now_col))

        if maze.isObjective(now_row, now_col):
            return now_path, len(explored)
        else:
            for neighbors in maze.getNeighbors(now_row, now_col):
                if neighbors not in explored:
                    frontier.append(now_path + [neighbors])  
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start_row, start_col = maze.getStart()
    goal_row, goal_col = maze.getObjectives()[0]
    path_set = queue.PriorityQueue()
    explored = set()
    ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
    ini_path = [maze.getStart()]
    path_set.put((ini_cost, ini_path))
    while not path_set.empty():
        min = path_set.get()
        # print(min)
        now_cost = min[0]
        now_path = min[1]
        now_row, now_col = now_path[-1]
        if (now_row, now_col) not in explored:
            explored.add((now_row, now_col))

        for neighbors in maze.getNeighbors(now_row, now_col):
            nei_row = neighbors[0]
            nei_col = neighbors[1]
            if neighbors not in explored:
                explored.add(neighbors)
                new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col)
                new_path = now_path + [neighbors]
                path_set.put((new_cost, new_path))

                if maze.isObjective(nei_row, nei_col):
                    return new_path, len(explored)
    return [], 0

# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     start_row, start_col = maze.getStart()
#     goal_row, goal_col = maze.getObjectives()[0]
#     print(maze.getObjectives())
#     path_set = queue.PriorityQueue()
#     explored = set()
#     ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
#     ini_path = [maze.getStart()]
#     path_set.put((ini_cost, ini_path))
#     while not path_set.empty():
#         min = path_set.get()
#         # print(min)
#         now_cost = min[0]
#         now_path = min[1]
#         now_row, now_col = now_path[-1]
#         if (now_row, now_col) not in explored:
#             explored.add((now_row, now_col))

#         for neighbors in maze.getNeighbors(now_row, now_col):
#             nei_row = neighbors[0]
#             nei_col = neighbors[1]
#             if neighbors not in explored:
#                 explored.add(neighbors)
#                 new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col) + len(now_path)
#                 new_path = now_path + [neighbors]
#                 path_set.put((new_cost, new_path))

#                 if maze.isObjective(nei_row, nei_col):
#                     return new_path, len(explored)
 
#     return [], 0

# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     # print(maze.getObjectives())
#     start = maze.getStart()
#     start_row, start_col = maze.getStart()
#     goal = maze.getObjectives()
#     goal_set = queue.PriorityQueue()
#     total_explored = set()
#     path = []
#     num_visited = 0
#     for items in goal:
#         dist = heuristic(items, start)
#         goal_set.put((dist, items))

#     while not goal_set.empty(): 
#         goal_now = goal_set.get()[1]
#         # print(start, goal_now)
#         goal_row, goal_col = goal_now
#         # print(maze.getObjectives())
#         path_set = queue.PriorityQueue()
#         explored = set()
#         # print(type(start_col), type(goal_col))
#         ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
#         ini_path = [start]
#         path_set.put((ini_cost, ini_path))
#         while not path_set.empty():
#             min = path_set.get()
#             # print(min)
#             now_cost = min[0]
#             now_path = min[1]
#             now = now_path[-1]
#             now_row, now_col = now_path[-1]
#             if now == goal_now:
#                 break
#             if (now_row, now_col) not in explored:
#                 explored.add((now_row, now_col))

#             if now not in total_explored:
#                 total_explored.add(now)

#             for neighbors in maze.getNeighbors(now_row, now_col):
#                 nei_row = neighbors[0]
#                 nei_col = neighbors[1]

#                 if neighbors not in total_explored:
#                     total_explored.add(neighbors)
                
#                 if neighbors not in explored:
#                     explored.add(neighbors)
#                     new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col) + len(now_path)
#                     new_path = now_path + [neighbors]
#                     path_set.put((new_cost, new_path))
                    
#                     if neighbors == goal_now:
#                         # print(neighbors, goal_now)
#                         # print(new_path)
#                         # return new_path, len(explored)
#                         break

                    
                    
#         # print(new_path)
#         path += new_path
#         # num_visited += len(explored)
#         start = goal_now
#         start_row, start_col = goal_now
#         num_visited = len(total_explored)
#         # print(total_explored)
#     return path, num_visited
#     return [], 0

def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    # print(maze.getObjectives())
    start = maze.getStart()
    start_row, start_col = maze.getStart()
    goal_list = maze.getObjectives()
    goal_set = queue.PriorityQueue()
    total_explored = set()
    path = []
    num_visited = 0
    for items in goal_list:
        dist = heuristic(items, start)
        goal_set.put((dist, items))

    while not goal_set.empty(): 
        # requeu the dist of dots to current start
        goal_set_new = goal_set
        goal_list_new = []
        while not goal_set_new.empty():
            
            goal_list_new.append(goal_set_new.get()[1])
        for items in goal_list_new:
            dist = heuristic(items, start)
            goal_set_new.put((dist, items))

        goal_now = goal_set_new.get()[1]
        
        print(start, goal_now)
        goal_row, goal_col = goal_now
        path_set = queue.PriorityQueue()
        explored = set()
        ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
        ini_path = [start]
        path_set.put((ini_cost, ini_path))
        while not path_set.empty():
            min = path_set.get()
            now_cost = min[0]
            now_path = min[1]
            now = now_path[-1]
            now_row, now_col = now_path[-1]
            if now == goal_now:
                break
            if (now_row, now_col) not in explored:
                explored.add((now_row, now_col))

            if now not in total_explored:
                total_explored.add(now)

            for neighbors in maze.getNeighbors(now_row, now_col):
                nei_row = neighbors[0]
                nei_col = neighbors[1]

                if neighbors not in total_explored:
                    total_explored.add(neighbors)
                
                if neighbors not in explored:
                    explored.add(neighbors)
                    new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col) + len(now_path)
                    new_path = now_path + [neighbors]
                    path_set.put((new_cost, new_path))
                    
                    if neighbors == goal_now:
                        break
                 
        print(new_path)
        path += new_path
        start = goal_now
        start_row, start_col = goal_now
        num_visited = len(total_explored)
    return path, num_visited
    return [], 0



# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored

#     frontier = queue.PriorityQueue() # in the form of ((row, col), f(n))
#     came_from = {} # record every waypoint's previous waypoint
#     cost_so_far = {} # in the form of ((row, col), g(n)), also functioned as explored set

#     start = maze.getStart()
#     goal = maze.getObjectives()[0]
#     print(start)
#     print(goal)
#     frontier.put(start, 0 + heuristic(goal, start))
    
#     came_from[start] = None
#     cost_so_far[start] = 0
 
#     while not frontier.empty():
#         current = frontier.get()
#         # print(current)
#         cur_row, cur_col = current
#         if current == goal:
#             # print(came_from)
#             # print(cost_so_far)
#             path = get_path(came_from, current)
#             return path, len(came_from)
        
#         for next in maze.getNeighbors(cur_row, cur_col):
#             new_cost = cost_so_far[current] + 1
#             if next not in cost_so_far or new_cost < cost_so_far[next]:
#                 cost_so_far[next] = new_cost
                
#                 priority = new_cost + heuristic(goal, next) # f(n) = h(n) + g(n)
#                 print(next, new_cost, priority)
#                 frontier.put(next, priority)
#                 # print(priority)
#                 came_from[next] = current
#                 if next == goal:
#                     # print(came_from)
#                     # print(cost_so_far)
#                     path = get_path(came_from, next)
#                     # print(frontier)
#                     # print(cost_so_far)
#                     return path, len(came_from)

#     return [], 0


def heuristic(goal, start):
    # calculate Manhattan distance h(n)
    goal_row, goal_col = goal
    start_row, start_col = start
    dist = abs(goal_row - start_row) + abs(goal_col - start_col)
    return dist

def get_path(came_from, current):
    # find the path from start to goal
    path = []
    while came_from[current] != None:
        path.append(current)
        current = came_from[current]
    path.append(current)
    path.reverse()
    return path
    

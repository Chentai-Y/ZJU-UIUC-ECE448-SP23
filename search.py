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
    # def dfs(maze, start, end, visited=None):
    #   if visited is None:
    #     visited = set()
    # visited.add(start)
    # if start == end:
    #     return True
    # for neighbor in maze.get_neighbors(start[0], start[1]):
    #     if neighbor not in visited:
    #         if dfs(maze, neighbor, end, visited):
    #             return True
    # return False


    bfs_waylist = [] # store all the possible ways
    bfs_waylist.append([maze.getStart()])
    visitnum = 0
    visit = set()

    while bfs_waylist is not None:
        #bfs-FIFO queue
        path = bfs_waylist.pop(0)
        # record if not visited/find next if visited
        if (path[-1]) in visit:
            continue
        if (path[-1]) not in visit:
            visit.add((path[-1]))
            visitnum += 1
        # find neighbors + path
        for target in maze.getNeighbors(path[-1][0], path[-1][1]):
            newpath = path + [target]
            if target not in visit:
                bfs_waylist.append(newpath)
        # output if goal
            if maze.isObjective(target[0],target[1]):
                visitnum += 1
                return [newpath, visitnum]
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    dfs_waylist = [] # store all the possible ways
    dfs_waylist.append([maze.getStart()])
    visitnum = 0
    visit = set() # mark visited position

    while dfs_waylist is not None:
        #dfs-LIFO stack
        path = dfs_waylist.pop(-1)
        # record if not visited/find next if visited
        if (path[-1]) in visit:
            continue
        if (path[-1]) not in visit:
            visit.add((path[-1]))
            visitnum += 1
        # find neighbors + path
        for target in maze.getNeighbors(path[-1][0], path[-1][1]):
            newpath = path + [target]
            if target not in visit:
                dfs_waylist.append(newpath)
        # output if goal
            if maze.isObjective(target[0],target[1]):
                visitnum += 1
                return [newpath, visitnum]
    return [], 0

import queue

def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    # write a pseudocode below:

    # def greedy(maze, start, end):
    #     current = start
    #     visited = set()
    #     path = [current]
        
    #     while current != end:
    #         visited.add(current)
    #         neighbors = maze.getNeighbors(current[0], current[1])
    #         next_cell = None
    #         min_distance = float('inf')
    #         for neighbor in neighbors:
    #             if neighbor not in visited:
    #                 distance = heuristic(neighbor, end)
    #                 if distance < min_distance:
    #                     next_cell = neighbor
    #                     min_distance = distance
    #         if next_cell is None:
    #             return None
    #         current = next_cell
    #         path.append(current)
    # return path

    greedy_ways = queue.PriorityQueue()  # the {cost,[path]} set queue, priorityqueue give a queue in sequence
    visit = set()
    visitnum = 0
    start_pos = maze.getStart()
    goal_pos = maze.getObjectives()[-1]
    cur_pos = start_pos
    Manhattan_distance = abs(cur_pos[0]-goal_pos[0]) + abs(cur_pos[1]-goal_pos[1])
    costfunc = Manhattan_distance  # c(n) = d(n) 
    greedy_ways.put((costfunc, [start_pos]))

    while cur_pos != goal_pos:

        cur_path = greedy_ways.get()[1]  # get the 1st priority item
        cur_pos = cur_path[-1]
        if cur_pos not in visit:
            visit.add(cur_pos)
            visitnum += 1
        for target in maze.getNeighbors(cur_pos[0],cur_pos[1]):
            if target not in visit:
                costfunc = abs(target[0]-goal_pos[0]) + abs(target[1]-goal_pos[1])
                greedy_ways.put((costfunc, cur_path + [target]))
            if target == goal_pos:
                return [cur_path + [target], visitnum+1]

    return [], 0




# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored

#     # def astar(maze, start, end):
#     # open_set = {start}
#     # came_from = {}
#     # g_score = {start: 0}
#     # f_score = {start: heuristic(start, end)}
#     # visited = set()

#     # while open_set:
#     #     current = min(open_set, key=lambda x: f_score[x])
#     #     if current == end:
#     #         path = [current]
#     #         while current in came_from:
#     #             current = came_from[current]
#     #             path.append(current)
#     #         path.reverse()
#     #         return path, visited
#     #     open_set.remove(current)
#     #     visited.add(current)
#     #     for neighbor in maze.get_neighbors(current[0], current[1]):
#     #         tentative_g_score = g_score[current] + 1
#     #         if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#     #             came_from[neighbor] = current
#     #             g_score[neighbor] = tentative_g_score
#     #             f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
#     #             if neighbor not in open_set:
#     #                 open_set.add(neighbor)
#     # return None, visited

#     Astar_ways = queue.PriorityQueue()  # the {cost,[path]} set queue, priorityqueue give a queue in sequence
#     visit = set()
#     visitnum = 0
#     start_pos = maze.getStart()
#     goal_pos = maze.getObjectives()[-1]
#     cur_pos = start_pos
#     Manhattan_distance = abs(cur_pos[0]-goal_pos[0]) + abs(cur_pos[1]-goal_pos[1])
#     costfunc = 0 + Manhattan_distance  # c(n) = g(n)+d(n) 
#     Astar_ways.put((costfunc, [start_pos]))
    
#     while cur_pos != goal_pos:

#         cur_path = Astar_ways.get()[1]  # get the 1st priority item
#         cur_pos = cur_path[-1]
#         if cur_pos not in visit:
#             visit.add(cur_pos)
#             visitnum += 1
#         for target in maze.getNeighbors(cur_pos[0],cur_pos[1]):
#             if target not in visit:
#                 costfunc = (len(cur_path)+1) + (abs(target[0]-goal_pos[0]) + abs(target[1]-goal_pos[1]))
#                 Astar_ways.put((costfunc, cur_path + [target]))
#             if target == goal_pos:
#                 return [cur_path + [target], visitnum+1]

#     return [], 0

# =================================== Astar for part2 ==============================================
# ==================================================================================================================================================


def find_next_goal(cur_pos, all_dots):
    Now_Manhattan = 0
    Last_Manhattan = float('inf')
    next_goal = ()
    for item in all_dots:
        Now_Manhattan = abs(cur_pos[0]-item[0]) + abs(cur_pos[1]-item[1])
        #Now_Manhattan = abs(((cur_pos[0]-item[0])**2+(cur_pos[1]-item[1])**2)**(1/2))
        if Last_Manhattan < Now_Manhattan:
            continue
        if Last_Manhattan >= Now_Manhattan:
            Last_Manhattan = Now_Manhattan
            next_goal = item
    all_dots.remove(next_goal)
    return next_goal,all_dots



def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    Astar_ways = queue.PriorityQueue()  # the {cost,[path]} queue, priorityqueue give a queue in sequence
    visit = set()
    visitnum = 0
    nodenum = 0
    expnode = 0
    start_pos = maze.getStart()
    all_dots = maze.getObjectives()
    cur_pos = start_pos
    finalpath = []
    last_all_dots = all_dots
    goal_pos, all_dots = find_next_goal(cur_pos, last_all_dots)

    

    Manhattan_distance = abs(cur_pos[0]-goal_pos[0]) + abs(cur_pos[1]-goal_pos[1])
    costfunc = 0 + Manhattan_distance  # c(n) = g(n)+d(n)
    Astar_ways.put((costfunc, [start_pos]))

    print("goal:",goal_pos, "dots:",all_dots)
    
    while last_all_dots is not None:
        

        if cur_pos == goal_pos:
            goal_pos, all_dots = find_next_goal(cur_pos, last_all_dots)
            Manhattan_distance = abs(cur_pos[0]-goal_pos[0]) + abs(cur_pos[1]-goal_pos[1])
            costfunc = 0 + Manhattan_distance  # c(n) = g(n)+d(n)
            Astar_ways.queue.clear()
            Astar_ways.put((costfunc, [cur_pos]))
            print (goal_pos)
            last_all_dots = all_dots
        
        if cur_pos != goal_pos:
            cur_path = Astar_ways.get()[1]  # get the 1st priority item
            cur_pos = cur_path[-1]
            if cur_pos not in visit:
                visit.add(cur_pos)
            for target in maze.getNeighbors(cur_pos[0],cur_pos[1]):
                print("inloop!")
                if target not in visit:
                    costfunc = (len(cur_path)+1) + (abs(target[0]-goal_pos[0]) + abs(target[1]-goal_pos[1]))
                    Astar_ways.put((costfunc, cur_path + [target]))
                    nodenum += 1
                    visitnum += 1
                if target == goal_pos:
                    finalpath = finalpath + cur_path
                    print("finalpath:",finalpath)
                    cur_pos = goal_pos
                    visit.clear()
                    
                    if nodenum >= 2:
                        expnode += 1
                        nodenum = 0
                    continue

        if not last_all_dots and cur_pos == goal_pos:
            print("last_all_dots empty")
            print(expnode)
            return [finalpath + [goal_pos], visitnum]

        
    return [], 0


















#============================================================frem CQZ========================================================







# # search.py
# # ---------------
# # Licensing Information:  You are free to use or extend this projects for
# # educational purposes provided that (1) you do not distribute or publish
# # solutions, (2) you retain this notice, and (3) you provide clear
# # attribution to the University of Illinois at Urbana-Champaign
# #
# # Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# # Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

# """
# This is the main entry point for MP1. You should only modify code
# within this file -- the unrevised staff files will be used for all other
# files and classes when code is run, so be careful to not modify anything else.
# """


# # Search should return the path and the number of states explored.
# # The path should be a list of tuples in the form (row, col) that correspond
# # to the positions of the path taken by your search algorithm.
# # Number of states explored should be a number.
# # maze is a Maze object based on the maze from the file specified by input filename
# # searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

# import queue

# def search(maze, searchMethod):
#     return {
#         "bfs": bfs,
#         "dfs": dfs,
#         "greedy": greedy,
#         "astar": astar,
#     }.get(searchMethod)(maze)


# def bfs(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     frontier = []
#     frontier.append([maze.getStart()])
#     explored = set()
#     while frontier:
#         now_path = frontier[0]
#         del frontier[0]
#         now_row, now_col = now_path[-1]
#         if (now_row, now_col) in explored:
#             continue     
#         else:  
#             explored.add((now_row, now_col))

#         if maze.isObjective(now_row, now_col):
#             return now_path, len(explored)
#         else:
#             for neighbors in maze.getNeighbors(now_row, now_col):
#                 if neighbors not in explored:
#                     frontier.append(now_path + [neighbors])
#     return [], 0


# def dfs(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     frontier = []
#     frontier.append([maze.getStart()])
#     explored = set()
#     while frontier:
#         now_path = frontier[-1]
#         del frontier[-1]
#         now_row, now_col = now_path[-1]
#         if (now_row, now_col) in explored:
#             continue     
#         else:  
#             explored.add((now_row, now_col))

#         if maze.isObjective(now_row, now_col):
#             return now_path, len(explored)
#         else:
#             for neighbors in maze.getNeighbors(now_row, now_col):
#                 if neighbors not in explored:
#                     frontier.append(now_path + [neighbors])  
#     return [], 0


# def greedy(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     start_row, start_col = maze.getStart()
#     goal_row, goal_col = maze.getObjectives()[0]
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
#                 new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col)
#                 new_path = now_path + [neighbors]
#                 path_set.put((new_cost, new_path))

#                 if maze.isObjective(nei_row, nei_col):
#                     return new_path, len(explored)
#     return [], 0

# # def astar(maze):
# #     # TODO: Write your code here
# #     # return path, num_states_explored
# #     start_row, start_col = maze.getStart()
# #     goal_row, goal_col = maze.getObjectives()[0]
# #     print(maze.getObjectives())
# #     path_set = queue.PriorityQueue()
# #     explored = set()
# #     ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
# #     ini_path = [maze.getStart()]
# #     path_set.put((ini_cost, ini_path))
# #     while not path_set.empty():
# #         min = path_set.get()
# #         # print(min)
# #         now_cost = min[0]
# #         now_path = min[1]
# #         now_row, now_col = now_path[-1]
# #         if (now_row, now_col) not in explored:
# #             explored.add((now_row, now_col))

# #         for neighbors in maze.getNeighbors(now_row, now_col):
# #             nei_row = neighbors[0]
# #             nei_col = neighbors[1]
# #             if neighbors not in explored:
# #                 explored.add(neighbors)
# #                 new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col) + len(now_path)
# #                 new_path = now_path + [neighbors]
# #                 path_set.put((new_cost, new_path))

# #                 if maze.isObjective(nei_row, nei_col):
# #                     return new_path, len(explored)
 
# #     return [], 0

# # def astar(maze):
# #     # TODO: Write your code here
# #     # return path, num_states_explored
# #     # print(maze.getObjectives())
# #     start = maze.getStart()
# #     start_row, start_col = maze.getStart()
# #     goal = maze.getObjectives()
# #     goal_set = queue.PriorityQueue()
# #     total_explored = set()
# #     path = []
# #     num_visited = 0
# #     for items in goal:
# #         dist = heuristic(items, start)
# #         goal_set.put((dist, items))

# #     while not goal_set.empty(): 
# #         goal_now = goal_set.get()[1]
# #         # print(start, goal_now)
# #         goal_row, goal_col = goal_now
# #         # print(maze.getObjectives())
# #         path_set = queue.PriorityQueue()
# #         explored = set()
# #         # print(type(start_col), type(goal_col))
# #         ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
# #         ini_path = [start]
# #         path_set.put((ini_cost, ini_path))
# #         while not path_set.empty():
# #             min = path_set.get()
# #             # print(min)
# #             now_cost = min[0]
# #             now_path = min[1]
# #             now = now_path[-1]
# #             now_row, now_col = now_path[-1]
# #             if now == goal_now:
# #                 break
# #             if (now_row, now_col) not in explored:
# #                 explored.add((now_row, now_col))

# #             if now not in total_explored:
# #                 total_explored.add(now)

# #             for neighbors in maze.getNeighbors(now_row, now_col):
# #                 nei_row = neighbors[0]
# #                 nei_col = neighbors[1]

# #                 if neighbors not in total_explored:
# #                     total_explored.add(neighbors)
                
# #                 if neighbors not in explored:
# #                     explored.add(neighbors)
# #                     new_cost = abs(nei_row - goal_row) + abs(nei_col - goal_col) + len(now_path)
# #                     new_path = now_path + [neighbors]
# #                     path_set.put((new_cost, new_path))
                    
# #                     if neighbors == goal_now:
# #                         # print(neighbors, goal_now)
# #                         # print(new_path)
# #                         # return new_path, len(explored)
# #                         break

                    
                    
# #         # print(new_path)
# #         path += new_path
# #         # num_visited += len(explored)
# #         start = goal_now
# #         start_row, start_col = goal_now
# #         num_visited = len(total_explored)
# #         # print(total_explored)
# #     return path, num_visited
# #     return [], 0

# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     # print(maze.getObjectives())
#     start = maze.getStart()
#     start_row, start_col = maze.getStart()
#     goal_list = maze.getObjectives()
#     goal_set = queue.PriorityQueue()
#     total_explored = set()
#     path = []
#     num_visited = 0
#     for items in goal_list:
#         dist = heuristic(items, start)
#         goal_set.put((dist, items))

#     while not goal_set.empty(): 
#         # requeu the dist of dots to current start
#         goal_set_new = goal_set
#         goal_list_new = []
#         while not goal_set_new.empty():
            
#             goal_list_new.append(goal_set_new.get()[1])
#         for items in goal_list_new:
#             dist = heuristic(items, start)
#             goal_set_new.put((dist, items))

#         goal_now = goal_set_new.get()[1]
        
#         print(start, goal_now)
#         goal_row, goal_col = goal_now
#         path_set = queue.PriorityQueue()
#         explored = set()
#         ini_cost = abs(start_row - goal_row) + abs(start_col - goal_col)
#         ini_path = [start]
#         path_set.put((ini_cost, ini_path))
#         while not path_set.empty():
#             min = path_set.get()
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
#                         break
                 
#         print(new_path)
#         path += new_path
#         start = goal_now
#         start_row, start_col = goal_now
#         num_visited = len(total_explored)
#     return path, num_visited
#     return [], 0



# # def astar(maze):
# #     # TODO: Write your code here
# #     # return path, num_states_explored

# #     frontier = queue.PriorityQueue() # in the form of ((row, col), f(n))
# #     came_from = {} # record every waypoint's previous waypoint
# #     cost_so_far = {} # in the form of ((row, col), g(n)), also functioned as explored set

# #     start = maze.getStart()
# #     goal = maze.getObjectives()[0]
# #     print(start)
# #     print(goal)
# #     frontier.put(start, 0 + heuristic(goal, start))
    
# #     came_from[start] = None
# #     cost_so_far[start] = 0
 
# #     while not frontier.empty():
# #         current = frontier.get()
# #         # print(current)
# #         cur_row, cur_col = current
# #         if current == goal:
# #             # print(came_from)
# #             # print(cost_so_far)
# #             path = get_path(came_from, current)
# #             return path, len(came_from)
        
# #         for next in maze.getNeighbors(cur_row, cur_col):
# #             new_cost = cost_so_far[current] + 1
# #             if next not in cost_so_far or new_cost < cost_so_far[next]:
# #                 cost_so_far[next] = new_cost
                
# #                 priority = new_cost + heuristic(goal, next) # f(n) = h(n) + g(n)
# #                 print(next, new_cost, priority)
# #                 frontier.put(next, priority)
# #                 # print(priority)
# #                 came_from[next] = current
# #                 if next == goal:
# #                     # print(came_from)
# #                     # print(cost_so_far)
# #                     path = get_path(came_from, next)
# #                     # print(frontier)
# #                     # print(cost_so_far)
# #                     return path, len(came_from)

# #     return [], 0


# def heuristic(goal, start):
#     # calculate Manhattan distance h(n)
#     goal_row, goal_col = goal
#     start_row, start_col = start
#     dist = abs(goal_row - start_row) + abs(goal_col - start_col)
#     return dist

# def get_path(came_from, current):
#     # find the path from start to goal
#     path = []
#     while came_from[current] != None:
#         path.append(current)
#         current = came_from[current]
#     path.append(current)
#     path.reverse()
#     return path
    

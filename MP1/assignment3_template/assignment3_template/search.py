# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP3. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
# Note that if you want to test one of your search methods, please make sure to return a blank list
#  for the other search methods otherwise the grader will not crash.
from collections import deque,OrderedDict
import heapq

class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): heuristic(i, j)
                for i, j in self.cross(objectives)
            }

    # Prim's algorithm adds edges to the MST in sorted order as long as they don't create a cycle
    def compute_mst_weight(self):
        weight      = 0
        for distance, i, j in sorted((self.distances[(i, j)], i, j) for (i, j) in self.distances):
            if self.unify(i, j):
                weight += distance
        return weight

    # helper checks the root of a node, in the process flatten the path to the root
    def resolve(self, key):
        path = []
        root = key
        while self.elements[root] is not None:
            path.append(root)
            root = self.elements[root]
        for key in path:
            self.elements[key] = root
        return root

    # helper checks if the two elements have the same root they are part of the same tree
    # otherwise set the root of one to the other, connecting the trees
    def unify(self, a, b):
        ra = self.resolve(a)
        rb = self.resolve(b)
        if ra == rb:
            return False
        else:
            self.elements[rb] = ra
            return True

    # helper that gets all pairs i,j for a list of keys
    def cross(self, keys):
        return (x for y in (((i, j) for j in keys if i < j) for i in keys) for x in y)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    dis = {}
    start = maze.start
    waypoints = deque()
    waypoints.extend(maze.waypoints)
    path = deque()
    indices = deque()
    indices.append(start)
    index = 0
    while (len(waypoints) > 0 ):
        state = indices[index]
        for i in range(len(waypoints)):
            if waypoints[i] == state:
                path.append(state)
                while state != start :
                    path.appendleft(dis[state])
                    state = dis[state]
                waypoints.rotate(-i)
                waypoints.popleft()
                break
        if (len(waypoints) == 0):
            break
        neighbors = maze.neighbors(state[0],state[1])
        for neighbor in neighbors:
            if ((maze.navigable(neighbor[0],neighbor[1]) == 1) and (neighbor not in indices)):
                indices.append(neighbor)
                dis[neighbor] = state
        index += 1
    
    return path

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    explored = deque()
    dis = {}
    start = maze.start
    # cost of each point
    cost = OrderedDict({start:0})
    waypoints = deque()
    # all destination
    waypoints.extend(maze.waypoints)
    # the path from start to end
    path = deque()
    # all indices that in the list but not visit
    indices = OrderedDict({start:0})
    
    
    while (len(waypoints) > 0):
        state = min(indices,key=indices.get)
        explored.append(indices.pop(state))
        for i in range(len(waypoints)):
            if waypoints[i] == state:
                path.append(state)
                while state != start :
                    path.appendleft(dis[state])
                    state = dis[state]
                waypoints.rotate(-i)
                waypoints.popleft()
                break
        if (len(waypoints) == 0):
            break
        neighbors = maze.neighbors(state[0],state[1])
        for neighbor in neighbors:
            if (neighbor in explored):
                continue
            if ((maze.navigable(neighbor[0],neighbor[1]) == 1) and (neighbor not in cost.keys())):
                dis[neighbor] = state
                cost[neighbor] = cost[state] + 1
                indices[neighbor] = cost[neighbor] + heuristic(waypoints[0],neighbor)
            elif (neighbor in cost.keys()):
                if(cost[neighbor] > cost[state] + 1):
                    cost[neighbor] = cost[state] + 1
                    dis[neighbor] = state
        
    
    
    
    return path

"""
return the manhatan distance between (i1,j1),(i2,j2)
"""
def heuristic(i,j):
    distance = abs(i[0]-j[0]) + abs(i[1]-j[1])
    return distance
    
    
    
    

def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # explored is the points have been visited
    # we have different status, each status own a cost, precedor, 
    # indices contains the points with different status, the key will be [(x,y),status]
    # to simplify, use the binary representation for status, the index is the sequence of the waypoints
    explored = deque()
    start = maze.start
    # cost of each point
    
    waypoints = deque()
    # all destination
    waypoints.extend(maze.waypoints)
    #prevent the repeat value
    waypoints = set(waypoints)
    
    status = tuple(waypoints)
    
    # the path from start to end
    path = deque()
    # MST instance for weighted the path
    precedor = {(start,status):0}
    # all indices that in the list but not visit
    indices = []
    start_point = [0,start,status]

    heapq.heappush(indices,start_point)
    cost = {(start,status):0}
    check_map = {}
    vertices = deque()
    for point in waypoints:
        vertices.clear()
        vertices.extend(waypoints)
        vertices.remove(point)
        mst = MST(vertices)
        map_status = tuple(vertices)
        check_map[map_status] = mst.compute_mst_weight()

    while (len(indices) > 0):

        point_state = heapq.heappop(indices)
        
        current_point = point_state[1]
        # current status of the current point
        current_status = point_state[2]
        state = (current_point,current_status)
        explored.append(state)
            # if a non-visit waypoiny is found in current status
#        if (current_point in current_status):
#                # type exchange in order to remove certain element
#            current_status = deque(current_status)
#            current_status.remove(current_point)
#            current_status = tuple(current_status)
#            # the new start point also consider as explored since we start from here
#            explored.append((current_point,current_status))
            
        # the first time we loop over all the waypoints, we find the path 
        
            
        # now add the neighbors to the indices
        
        neighbors = maze.neighbors(current_point[0],current_point[1])
        for neighbor in neighbors:
            current_status = point_state[2]
            if (neighbor in current_status):
                current_status = deque(current_status)
                current_status.remove(neighbor)
                current_status = tuple(current_status)
                if (len(current_status) == 0):
                    path.appendleft(neighbor)
            #to prevent the case of cycle
                    while (state != precedor[state]):
                        path.appendleft(current_point)
                        # trace back with the first point that touch the last waypoint
                        state = precedor[state]
                        # make sure only quit when reach the very begin
                        if (state == 0):
                            return path
                        current_point = state[0]
                    break
            # set the point to preset format
            check = (neighbor,current_status)
            if (check in explored):
                continue
            # only go to the point that is navigatable
            elif ( check not in cost.keys()):
                precedor[check] = state
                cost[check] = cost[state] + 1
                # if more than one waypoints, need to consider the mst
                if (len(current_status) > 1):
                    dis = abs(current_status[0][0]-neighbor[0])+abs(current_status[0][1]-neighbor[1])
                    #end = current_status[0]
                    #vertices.clear()
                    for point in current_status:
                        if (dis == 1):
                            break
                        elif(abs(point[0]-neighbor[0])+abs(point[1]-neighbor[1]) < dis):
                            dis = abs(point[0]-neighbor[0])+abs(point[1]-neighbor[1])
                            #end = point

                    #vertices.extend(current_status)
                    #vertices.remove(end)
                    #map_status = tuple(vertices)
                    if (current_status not in check_map.items()):
                        mst = MST(current_status)
                        check_map[current_status] = mst.compute_mst_weight()*1.19
                    way_cost = cost[check] + dis + check_map[current_status]
                    now = [way_cost,neighbor,current_status]
                    heapq.heappush(indices,now)
                    
                # only one waypoint left, the same as single
                else:
                    way_cost = cost[check] + abs(current_status[0][0]-neighbor[0])+abs(current_status[0][1]-neighbor[1])
                    now = [way_cost,neighbor,current_status]
                    heapq.heappush(indices,now)
             #this part is for renewing the cost in the list 
            else:
                # renew the cost of points that haven been visited
                if (cost[check] > cost[state]  + 1):
                    cost[check] = cost[state] + 1
                    precedor[check] = state
                    #for i in range(len(indices)):
                    #    if (indices[i] == now):
                    if (len(current_status) > 1):
                        dis = abs(current_status[0][0]-neighbor[0])+abs(current_status[0][1]-neighbor[1])
                        #end = current_status[0]
                        #vertices.clear()
                        for point in current_status:
                            if (dis == 1):
                                break
                            elif(abs(point[0]-neighbor[0])+abs(point[1]-neighbor[1]) < dis):
                                dis = abs(point[0]-neighbor[0])+abs(point[1]-neighbor[1])
                                #end = point
                        #vertices.extend(current_status)
                        #vertices.remove(end)
                        #map_status = tuple(vertices)
                        if (current_status not in check_map.items()):
                            mst = MST(current_status)
                            check_map[current_status] = mst.compute_mst_weight()*1.19
                        way_cost = check_map[current_status] + cost[state] + 1
                        now = [way_cost,neighbor,current_status]
                        heapq.heappush(indices,now)
                    else:
                        way_cost = cost[check] + abs(current_status[0][0]-neighbor[0])+abs(current_status[0][1]-neighbor[1])
                        now = [way_cost,neighbor,current_status]
                        heapq.heappush(indices,now)
                    

    
    # fail to find a path, return empty
    return []
#    precedor = {}
#    start = maze.start
#    # cost of each point
#    cost = OrderedDict({start:0})
#    waypoints_origin = deque()
#    # all destination
#    waypoints_origin.extend(maze.waypoints)
#    # the path from start to end
#    path = deque()
#    output = deque()
#    # MST instance for weighted the path
#    # all indices that in the list but not visit
#    indices = OrderedDict({start:0}) 
#    check_map_origin = {}
#    
#    length = 1000000000
#    for point in waypoints_origin:
#        vertices = deque()
#        vertices.extend(waypoints_origin)
#        vertices.remove(point)
#        mst = MST(vertices)
#        check_map_origin[point] = mst.compute_mst_weight()
#    for point in waypoints_origin:
#        precedor = {}
#        start = maze.start
#        # cost of each point
#        cost = OrderedDict({start:0})
#        waypoints = deque()
#        # all destination
#        waypoints.extend(maze.waypoints)
#        # the path from start to end
#        path = deque()
#        output = deque()
#        # MST instance for weighted the path
#        # all indices that in the list but not visit
#        indices = OrderedDict({start:0}) 
#        check_map = check_map_origin
#        
#        length = 1000000000
#        
#        check_map[point] = 0
#        
#        while (len(waypoints) > 0):
#        
#            state = min(indices,key=indices.get)
#            indices.pop(state)
#            for i in range(len(waypoints)):
#                if waypoints[i] == state:
#                    new_path = deque()
#                    way = state
#                    while way != start :
#                        new_path.appendleft(way)
#                        way = precedor[way]
#                    path.extend(new_path)
#                    waypoints.rotate(-i)
#                    
#                    waypoints.popleft()
#                    
#                    start = state
#                    # renew the cost and precedor
#                    cost = OrderedDict({start:0})
#                    precedor = {}
#                    indices = OrderedDict({start:0}) 
#                    #first load all map first
#                    check_map = {}
#                    for point in waypoints:
#                        vertices = deque()
#                        vertices.extend(waypoints)
#                        vertices.remove(point)
#                        mst = MST(vertices)
#                        check_map[point] = mst.compute_mst_weight()
#                    break
#            if (len(waypoints) == 0):
#                break
#            neighbors = maze.neighbors(state[0],state[1])
#            for neighbor in neighbors:
#                if ((maze.navigable(neighbor[0],neighbor[1]) == 1) and (neighbor not in cost.keys())):
#                    precedor[neighbor] = state
#                    cost[neighbor] = cost[state] + 1
#                    # if more than one waypoints, need to consider the mst
#                    if (len(waypoints) > 1):
#                        dis = 10000000000
#                        for point in waypoints:
#                            distance = heuristic(point,neighbor)
#                            value = distance + check_map[point]
#                       
#                        if(value < dis):
#                            dis = value
#                        
#                        indices[neighbor] = cost[neighbor] + dis 
#                    
#                # only one waypoint left, the same as single
#                    else:
#                        indices[neighbor] = cost[neighbor] + heuristic(waypoints[0],neighbor) 
#    # add the start to begin
#        path.appendleft(maze.start)
#        if (len(path) < length):
#            length = len(path)
#            output = path
#    return output

def fast(maze):
    """
    Runs suboptimal search algorithm for extra credit/part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
#    explored = deque()
#    precedor = {}
#    start = maze.start
#    # cost of each point
#    cost = OrderedDict({start:0})
#    waypoints = deque()
#    # all destination
#    waypoints.extend(maze.waypoints)
#    # the path from start to end
#    path = deque()
#    # MST instance for weighted the path
#
#    # all indices that in the list but not visit
#    indices = OrderedDict({start:0})  
#    while (len(waypoints) > 0):
#        
#        state = min(indices,key=indices.get)
#        explored.append(indices.pop(state))
#        for i in range(len(waypoints)):
#            if waypoints[i] == state:
#                new_path = deque()
#                way = state
#                while way != start :
#                    new_path.appendleft(way)
#                    way = precedor[way]
#                path.extend(new_path)
#                waypoints.rotate(-i)
#                
#                waypoints.popleft()
#                
#                start = state
#                # renew the cost and precedor
#                cost = OrderedDict({start:0})
#                precedor = {}
#                indices = OrderedDict({start:0}) 
#                break
#        if (len(waypoints) == 0):
#            break
#        neighbors = maze.neighbors(state[0],state[1])
#        for neighbor in neighbors:
#            if (neighbor in explored):
#                if (cost[neighbor] > cost[state] + 1):
#                    explored.remove(neighbor)
#                    dis = 100000000
#                    for point in waypoints:
#                        if(heuristic(point,neighbor) < dis):
#                            dis = heuristic(point,neighbor)
#                            end = point
#                    vertices = deque()
#                    vertices.extend(waypoints)
#                    vertices.remove(end)
#                    mst = MST(vertices)
#                    indices[neighbor] = mst.compute_mst_weight() + cost[neighbor] + cost[state] + 1
#                    cost[neighbor] = cost[state] + 1
#                    precedor[neighbor] = state
#                continue
#            if ( maze.navigable(neighbor[0],neighbor[1]) == 1 and neighbor not in cost.keys()):
#                precedor[neighbor] = state
#                cost[neighbor] = cost[state] + 1
#                # if more than one waypoints, need to consider the mst
#                if (len(waypoints) > 1):
#                    dis = 10000000000
#                    vertices = deque()
#                    for point in waypoints:
#                        if(heuristic(point,neighbor) < dis):
#                            dis = heuristic(point,neighbor)
#                            end = point
#                            # using the rest points to calculate the distance
#                            # if we have two waypoints are the same far from this point, we use the small one 
#                    vertices.extend(waypoints)
#                    vertices.remove(end)
#                    mst = MST(vertices)
#                        
#                    indices[neighbor] = cost[neighbor] + dis + mst.compute_mst_weight() + diagonal(neighbor,end)
#                    
#                # only one waypoint left, the same as single
#                else:
#                    indices[neighbor] = cost[neighbor] + heuristic(waypoints[0],neighbor) + diagonal(neighbor,end)
#
#            elif(neighbor in cost.keys()):
#                if (cost[neighbor] > cost[state] + 1):
#                    indices[neighbor] = indices[neighbor] - cost[neighbor] + cost[state] + 1
#                    cost[neighbor] = cost[state] + 1
#                    precedor[neighbor] = state
#                    
#    return path

    explored = deque()
    start = maze.start
    # cost of each point
    
    waypoints = deque()
    # all destination
    waypoints.extend(maze.waypoints)
    #prevent the repeat value
    waypoints = set(waypoints)

    status = tuple(waypoints)
    
    # the path from start to end
    path = deque()
    # MST instance for weighted the path
    precedor = {(start,status):0}
    # all indices that in the list but not visit
    indices = []
    start_point = [0,start,status]

    heapq.heappush(indices,start_point)
    cost = {(start,status):0}
    check_map = {}
    vertices = deque()
    for point in waypoints:
        vertices.clear()
        vertices.extend(waypoints)
        vertices.remove(point)
        mst = MST(vertices)
        map_status = tuple(vertices)
        check_map[map_status] = mst.compute_mst_weight()

    while (len(indices) > 0):

        point_state = heapq.heappop(indices)
        
        current_point = point_state[1]
        # current status of the current point
        current_status = point_state[2]
        state = (current_point,current_status)
        explored.append(state)
            # if a non-visit waypoiny is found in current status
#        if (current_point in current_status):
#                # type exchange in order to remove certain element
#            current_status = deque(current_status)
#            current_status.remove(current_point)
#            current_status = tuple(current_status)
#            # the new start point also consider as explored since we start from here
#            explored.append((current_point,current_status))
            
        # the first time we loop over all the waypoints, we find the path 
        
            
        # now add the neighbors to the indices
        
        neighbors = maze.neighbors(current_point[0],current_point[1])
        for neighbor in neighbors:
            current_status = point_state[2]
            if (neighbor in current_status):
                current_status = deque(current_status)
                current_status.remove(neighbor)
                current_status = tuple(current_status)
                if (len(current_status) == 0):
                    path.appendleft(neighbor)
            #to prevent the case of cycle
                    while (state != precedor[state]):
                        path.appendleft(current_point)
                        # trace back with the first point that touch the last waypoint
                        state = precedor[state]
                        # make sure only quit when reach the very begin
                        if (state == 0):
                            return path
                        current_point = state[0]
                    break
            # set the point to preset format
            check = (neighbor,current_status)
            if (check in explored):
                continue
            # only go to the point that is navigatable
            elif ( check not in cost.keys()):
                precedor[check] = state
                cost[check] = cost[state] + 1
                # if more than one waypoints, need to consider the mst
                if (len(current_status) >= 1):
                    dis = heuristic(current_status[0],neighbor)*2
                    #end = current_status[0]
                    #vertices.clear()
                    for point in current_status:
                        if (dis == 0):
                            break
                        elif(heuristic(point,neighbor)*2 < dis):
                            dis =  heuristic(point,neighbor)*2
                            #end = point

                    #vertices.extend(current_status)
                    #vertices.remove(end)
                    #map_status = tuple(vertices)
                    if (current_status not in check_map.items()):
                        mst = MST(current_status)
                        check_map[current_status] = mst.compute_mst_weight()*2.45
                    way_cost = cost[check] + dis*2 + check_map[current_status]
                    now = [way_cost,neighbor,current_status]
                    heapq.heappush(indices,now)
                    
                # only one waypoint left, the same as single
                else:
                    way_cost = cost[check] + heuristic(current_status[0],neighbor)*2
                    now = [way_cost,neighbor,current_status]
                    heapq.heappush(indices,now)
             #this part is for renewing the cost in the list 
            else:
                # renew the cost of points that haven been visited
                if (cost[check] > cost[state]  + 1):
                    cost[check] = cost[state] + 1
                    precedor[check] = state
                    #for i in range(len(indices)):
                    #    if (indices[i] == now):
                    if (len(current_status) > 1):
                        dis =  heuristic(point,neighbor)*2
                        #end = current_status[0]
                        #vertices.clear()
                        for point in current_status:
                            if (dis == 0):
                                break
                            elif( heuristic(point,neighbor)*2 < dis):
                                dis =  heuristic(point,neighbor)*2
                                #end = point
                        #vertices.extend(current_status)
                        #vertices.remove(end)
                        #map_status = tuple(vertices)
                        if (current_status not in check_map.items()):
                            mst = MST(current_status)
                            check_map[current_status] = mst.compute_mst_weight()*2.45
                        way_cost = check_map[current_status] + cost[state] + 1
                        now = [way_cost,neighbor,current_status]
                        heapq.heappush(indices,now)
                    else:
                        way_cost = cost[check] + heuristic(current_status[0],neighbor)*2#+diagonal(current_status[0],neighbor)
                        now = [way_cost,neighbor,current_status]
                        heapq.heappush(indices,now)
                    

    
    # fail to find a path, return empty
    return []
    
    

def diagonal(i,j):
    distance = ((i[0]-j[0])**2 + (i[1]-j[1])**2)**0.5
    return distance

# find a MST graph generating and cost calculating algorithm
class Graph:
    def __init__(self, vertex):
        self.V = vertex
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def search(self, parent, i):
        if parent[i] == i:
            return i
        return self.search(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.search(parent, x)
        yroot = self.search(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            i = i + 1
            x = self.search(parent, u)
            y = self.search(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        return result

# find from github an algorithm to calculate the mst length
def cal_MST_cost(wp_list):


    size = len(wp_list)
    if size == 1 or size == 0:
        return 0

    g = Graph(size)
    for node1 in range(size):
        for node2 in range(size):
            if node2 == node1:
                continue  # skip edge if dest, source are the same node
            g.add_edge(node1, node2, heuristic(wp_list[node1], wp_list[node2]))

    cost = 0
    for edge in g.kruskal():
        cost += edge[2]
    return cost
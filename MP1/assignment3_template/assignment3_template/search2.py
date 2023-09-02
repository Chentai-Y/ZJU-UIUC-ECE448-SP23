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
def Manht_dis(pt1,pt2):
    return(abs(pt1[0]-pt2[0]) + abs(pt1[1]- pt2[1]))

# Feel free to use the code below as you wish
# Initialize it with a list/tuple of objectives
# Call compute_mst_weight to get the weight of the MST with those objectives
# TODO: hint, you probably want to cache the MST value for sets of objectives you've already computed...
# Note that if you want to test one of your search methods, please make sure to return a blank list
#  for the other search methods otherwise the grader will not crash.
class MST:
    def __init__(self, objectives):
        self.elements = {key: None for key in objectives}

        # TODO: implement some distance between two objectives
        # ... either compute the shortest path between them, or just use the manhattan distance between the objectives
        self.distances   = {
                (i, j): Manht_dis(i, j)
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



from collections import deque
import heapq


def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return_path = []
    explored_set = []
    parents = {}
    frontier = deque()
    frontier.append(maze.start)
    parents[maze.start] = (-1,-1)
    # print(maze.start)
    try:
        while(1):
            search_node = frontier.popleft()
            # print(search_node)
            explored_set.append(search_node)
            search_node_neighbors = maze.neighbors(search_node[0],search_node[1])
            for appended_node in search_node_neighbors:
                if((appended_node in explored_set) or 
                    (appended_node in frontier)):
                    continue
                if(appended_node == maze.waypoints[0]):
                    parents[appended_node] = search_node
                    frontier.append(appended_node)
                    raise StopIteration # jump out of the while and for loop
                
                frontier.append(appended_node)
                parents[appended_node] = search_node
            if(len(frontier) == 0):
                print("the path is not found!")
                return []
    
    except StopIteration:
        pass
    
    # print("path to waypoints find!")
    # recover the path
    start_pt = maze.waypoints[0]
    # print('start point:',maze.start)
    # print(start_pt)
    while(start_pt != (-1,-1)):
        return_path.append(start_pt)
        start_pt = parents[start_pt]
    
    return_path.reverse()
    # print(return_path)
    return return_path 


def Back_trace(path,parents,end_point,start_point):
    while(start_point != end_point):
        path.append(start_point)
        start_point = parents[start_point]
    
    return path.reverse()

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    path = []
    parents = {}
    explored_dist = {}
    frontier = []
    g_n = 0
    h_n = Manht_dis(maze.start,maze.waypoints[0])
    heap_tuple = (g_n+h_n,maze.start)
    heapq.heappush(frontier,heap_tuple)
    parents[maze.start] = (-1,-1)
    explored_dist[maze.start] = 0
    while(1):
        detect_node = heapq.heappop(frontier)[1]
        # print(detect_node)
        nbs = maze.neighbors(detect_node[0],detect_node[1])
        if(detect_node in maze.waypoints):
            break
        for appended_node in nbs:
            g_n = explored_dist[detect_node] + 1
            
            if (appended_node not in explored_dist.keys()):
                h_n = Manht_dis(appended_node,maze.waypoints[0])
                heap_tuple = (g_n + h_n , appended_node)
                heapq.heappush(frontier,heap_tuple)
                parents[appended_node] = detect_node
                explored_dist[appended_node] = g_n
            
            elif g_n < explored_dist[appended_node]:
                h_n = Manht_dis(appended_node,maze.waypoints[0])
                heap_tuple = (g_n + h_n, appended_node)
                heapq.heappush(frontier,heap_tuple)
                parents[appended_node] = detect_node
                explored_dist[appended_node] = g_n

    
    Back_trace(path,parents,(-1,-1),maze.waypoints[0])
    return path

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
def cal_MST_cost(waypoints, wp_bitmap_tuple):
    wp_bitmap = list(wp_bitmap_tuple)
    wp_list = []
    for i in range(len(wp_bitmap)):
        if wp_bitmap[i] == 0:
            wp_list.append(waypoints[i])

    size = len(wp_list)
    if size == 1 or size == 0:
        return 0

    g = Graph(size)
    for node1 in range(size):
        for node2 in range(size):
            if node2 == node1:
                continue  # skip edge if dest, source are the same node
            g.add_edge(node1, node2, Manht_dis(wp_list[node1], wp_list[node2]))

    cost = 0
    for edge in g.kruskal():
        cost += edge[2]
    return cost

def compute_cloest(waypoints, reached_array, current_pt):
    select_list = []
    for i in range(len(reached_array)):
        if reached_array[i] == 0:
            select_list.append(Manht_dis(waypoints[i],current_pt))
    
    return select_list

def astar_multiple(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    ret_path = []
    reached_wpt = []
    parents = {}
    explored_dist = {}
    mst_cost_cache = {}
    frontier = []

    for wpt in maze.waypoints:
        reached_wpt.append(0)

    closest_wp = compute_cloest(maze.waypoints,reached_wpt,maze.start)

    current_state = (maze.start,tuple(reached_wpt))
    mst_cost_cache[current_state[1]] = cal_MST_cost(maze.waypoints,current_state[1])
    MST_length = mst_cost_cache[current_state[1]]
    print(MST_length)
    heap_tuple = (min(closest_wp) + MST_length , current_state)
    heapq.heappush(frontier,heap_tuple)
    # frontier_state[current_state] = 0

    parents[current_state] = -1
    explored_dist[current_state] = 0

    while(1):
        frontier_pt = heapq.heappop(frontier)
        # print(frontier_pt)
        min_state = frontier_pt[1]
        # print("min state",min_state)
        detect_node = min_state[0]
        # if(min_state[0] == (5,4)):
        #     print("line 254", frontier_pt)
        # if(min_state[0] == (4,4)):
        #     print("line 254", frontier_pt)
        # if(min_state[0] == (3,4)):
        #     print("line 254", frontier_pt)
        nbs = maze.neighbors(detect_node[0],detect_node[1])

        if sum(min_state[1]) == len(maze.waypoints):
            current_state = min_state
            # print(detect_node)
            break

        for appended_node in nbs:
            g_n = explored_dist[min_state] + 1
            # find a waypoint
            old_reached_pt = list(min_state[1])
            if appended_node in maze.waypoints:
                old_index = maze.waypoints.index(appended_node)
                old_reached_pt[old_index] = 1
            
            new_reached_pt = tuple(old_reached_pt)
            current_state = (appended_node,new_reached_pt)

            # case for unexplored node
            if (current_state not in explored_dist.keys()):

                # case for unexplored 
                if current_state[1] not in mst_cost_cache.keys():
                    mst_cost_cache[current_state[1]] = cal_MST_cost(maze.waypoints,current_state[1])
                MST_length = mst_cost_cache[current_state[1]]

                d_list = compute_cloest(maze.waypoints,new_reached_pt,appended_node)
                # print(f_n)
                if(len(d_list) == 0):
                    d_list.append(0)
                f_n = min(d_list) + MST_length + g_n
                heap_tuple = (f_n,current_state)
                # print(heap_tuple)
                # if(current_state[0] == (3,4)):
                #     print(min_state)
                #     print("line 290", heap_tuple)
                heapq.heappush(frontier,heap_tuple)
                parents[current_state] = min_state
                explored_dist[current_state] = g_n
                # frontier_state[current_state] = 0
                # if(current_state[0] == (5,4)):
                #     print(current_state)
                #     print(min_state)

            # case for explored node
            elif g_n < explored_dist[current_state]:

                # adding new cache value
                if current_state[1] not in mst_cost_cache.keys():
                    mst_cost_cache[current_state[1]] = cal_MST_cost(maze.waypoints,current_state[1])
                MST_length = mst_cost_cache[current_state[1]]
                d_list = compute_cloest(maze.waypoints,new_reached_pt,appended_node)
                # print(f_n)
                if(len(d_list) == 0):
                    d_list.append(0)
                f_n = min(d_list) + MST_length + g_n
                heap_tuple = (f_n,current_state)
                heapq.heappush(frontier,heap_tuple)
                parents[current_state] = min_state
                explored_dist[current_state] = g_n
                # if(current_state[0] == (5,4)):
                #     print(current_state)
                #     print(min_state)
    
    back_state = current_state
    # back trace
    while back_state != -1:
        # print(back_state)
        ret_path.append(back_state[0])
        back_state = parents[back_state]
    ret_path.reverse()
    # print(ret_path)
    # print(reached_wpt)
    # print(parents[((1, 24), (1, 1, 1, 1, 1, 1, 0))])
    return ret_path

def fast(maze):
    """
    Runs suboptimal search algorithm for extra credit/part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []



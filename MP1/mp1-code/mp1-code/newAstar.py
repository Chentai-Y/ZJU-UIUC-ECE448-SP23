# ==================================================================================================================================================
# NEW astar created 2023/3/13
# modified 3/13/14:16
import queue

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
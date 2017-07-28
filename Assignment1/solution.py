#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems

#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''       
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
  return count

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''      
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    manhattan_sum = 0 #Sum of Manhattan Distances
    for box in state.boxes: #Iterate through each box
        distance = []
        if box in state.storage and (state.restrictions is None or box in state.restrictions[state.boxes[box]]): #If shortest distance = 0, then don't calculate
            pass
        else: # Otherwise, continue the Manhattan Distance calculations
            if state.restrictions is not None: # state has restrictions, so check valid storages
                for storage in state.restrictions[state.boxes[box]]: #Iterate through the storage locations
                    distance.append(abs(storage[0] - box[0]) + abs(storage[1] - box[1]))
                manhattan_sum += min(distance)
            else: # no restrictions, check all storages
                for storage in state.storage: #Iterate through the storage locations
                    distance.append(abs(storage[0] - box[0]) + abs(storage[1] - box[1]))
                manhattan_sum += min(distance)
    return manhattan_sum

def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #heur_manhattan_distance has flaws.   
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    result = 0 # Result that will be returned.

    # Figure out where all the obstacles are.
    obstacles = []
    for x in range (-1,state.width):
      obstacles.append((x,-1))
      obstacles.append((x,state.height))
    for y in range (-1,state.height):
      obstacles.append((-1,y))
      obstacles.append((state.width,y))
    for z in state.obstacles:
      obstacles.append(z)
    
    for box in state.boxes: #Iterate through each box.
        if (box[0] + 1, box[1]) in obstacles and (box[0], box[1] + 1) in obstacles and box not in state.storage:
          result = float("inf")
          break
        if (box[0] - 1, box[1]) in obstacles and (box[0], box[1] + 1) in obstacles and box not in state.storage:
          result = float("inf")
          break
        if (box[0] + 1, box[1]) in obstacles and (box[0], box[1] - 1) in obstacles and box not in state.storage:
          result = float("inf")
          break
        if (box[0] - 1, box[1]) in obstacles and (box[0], box[1] - 1) in obstacles and box not in state.storage:
          result = float("inf")
          break
        distance = []
        for storage in state.storage: #Iterate through the storage locations.
            distance.append(abs(storage[0] - box[0]) + abs(storage[1] - box[1]))
            for robot in state.robot:
                distance.append(abs(robot - box[0]) + abs(robot - box[1]))
            result = result + min(distance)

    return result

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    
    return sN.gval + (weight * sN.hval)

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False''' 

    # Initiate the search engine.
    search_engine = SearchEngine('best_first', 'full')
    search_engine.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn)
    
    # Take a note of the start time.
    start = os.times()[0]
    
    goal = search_engine.search(timebound) # Goal state.
    
    if goal:
        costbound = goal.gval # Costbound.
        time_remaining = timebound - (os.times()[0] - start)
        best = goal
        while time_remaining > 0 and not search_engine.open.empty: # While there is still time.
            initial_time = os.times()[0]
            new_goal = search_engine.search(time_remaining, costbound = (costbound, float("inf"), float("inf")))
            time_remaining = time_remaining - (os.times()[0] - initial_time) # Update remaining time.
            if new_goal:
                costbound = new_goal.gval
                best = new_goal
        return best # Return the best state.
    else:
        return False


def anytime_weighted_astar(initial_state, heur_fn, weight, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    # Initiate the search engine.
    search_engine = SearchEngine('custom', 'full')
    search_engine.init_search(initial_state, goal_fn = sokoban_goal_state, heur_fn = heur_fn, fval_function = (lambda sN: fval_function(sN, 1)))
    
    # Take a note of the start time.
    start = os.times()[0]
    
    goal = search_engine.search(timebound) # Goal state.
    
    if goal:
        costbound = goal.gval + heur_fn(goal) # Costbound.
        time_remaining = timebound - (os.times()[0] - start)
        best = goal
        while time_remaining > 0: # While there is still time.
            initial_time = os.times()[0]
            new_goal = search_engine.search(time_remaining, costbound = (float("inf"), float("inf"), costbound))
            time_remaining = time_remaining - (os.times()[0] - initial_time) # Update remaining time.
            if new_goal:
                costbound = new_goal.gval + heur_fn(new_goal)
                best = new_goal
    
        return best # Return the best state.
    else:
        return False


if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_displaced)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit 
  print("Running Anytime Weighted A-star")   

  for i in range(0, 10):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 




# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

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


def pathback (parent, start, end, pathVert):
    print("PATHHHHH",pathVert)
    path = [end]
    while path[-1] != start:
        state = path[-1]
        print("state", state)
        path.remove(path[-1])
        retval = parent[state]
        print("rv:", retval)
        k = (retval, state)
        pathapp = pathVert[k]
        print("pa", pathapp)
        print(type(pathapp))
        par = pathapp[::-1]
        print("par", par)
        path += par
        print("mid paths", path)
    path.reverse()
    print(path)
    return path

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        key = path[-1]
        retVal= parent[key]
        path.append(retVal)
    path.reverse()
    return path
def manhattan(point1,point2):
    return abs(point1[0] - point2[0]) + abs(point1[1]-point2[1])


def manhattanOptimised (point1, goalsList, distances):
    #max1 = 0
    #max2 = 0
    maxdist = 0

    #for i in goalsList:
     #   length = abs(point1[0] - i[0]) + abs(point1[1] - i[1])
      #  if length > max1:
      #      max1 = length
      #  elif length > max2:
       #     max2 = length

    for i in goalsList:
        for j in goalsList:
            if i != j:
                if maxdist < distances[(i, j)]:
                    maxdist = distances[(i, j)]
                    first = i
                    second = j

    if(len(goalsList) >=2):
        length1 = abs(point1[0] - first[0]) + abs(point1[1] - first[1])
        length2 = abs(point1[0] - second[0]) + abs(point1[1] - second[1])

        if(length1 < length2):
            return maxdist + length1
        else:
            return maxdist + length2
    else:
        return abs(point1[0] - goalsList[0][0]) + abs(point1[1] - goalsList[0][1])
    #print("Md ",maxdist)
   # print("max2 ", max2)
   # return maxdist + max2


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    startState = maze.getStart()
    goalState  = maze.getObjectives()
    (row, col) = maze.getDimensions()
    noOfStatesVisited = 1
    parent = {}
    Myqueue = queue.Queue(0)
    pathTraversed = []
    visited = []
    visited.append(startState)
    Myqueue.put(startState)

    while not Myqueue.empty():
        currentState = Myqueue.get()
        print(currentState)
        neighbors = maze.getNeighbors(currentState[0], currentState[1])
        print(neighbors)
        for nbrs in neighbors:
            if nbrs not in visited:
                Myqueue.put(nbrs)
                visited.append(nbrs)
                noOfStatesVisited += 1
                parent[nbrs] = currentState

            if nbrs in goalState:
                path = backtrace(parent, startState, nbrs)
                pathTraversed += path
                startState = nbrs
                Myqueue = queue.Queue(0)
                Myqueue.put(startState)
                goalState.remove(nbrs)
                visited = []
                parent = {}
                if goalState:
                    break
                else:
                    return pathTraversed, noOfStatesVisited




def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    startState = maze.getStart()
    goalState = maze.getObjectives()
    (row, col) = maze.getDimensions()
    noOfStatesVisited = 1
    parent = {}
    Mystack = []

    visited = []
    visited.append(startState)
    Mystack.append(startState)

    while Mystack != []:
        currentState = Mystack.pop()

        neighbors = maze.getNeighbors(currentState[0], currentState[1])
        for nbrs in neighbors:
            print(Mystack)
            if nbrs not in visited:
                Mystack.append(nbrs)
                visited.append(nbrs)
                noOfStatesVisited += 1
                parent[nbrs] = currentState

            if nbrs == goalState:
                break

    pathTraversed = backtrace(parent, startState, goalState[0])
    return pathTraversed, noOfStatesVisited


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    goalState = maze.getObjectives()
    startState = maze.getStart()
    openSet = set()
    (row, col) = maze.getDimensions()
    h = [[0 for i in range(col)] for j in range(row)]
    pathTraversed = []
    noOfStatesVisited = 1
    parent = {}
    visited =[]
    minH = 100000000
    currentState = startState
    minState = (-1,-1)

    openSet.add(startState)
    while openSet:

        currentState = min(openSet, key=lambda o: h[o[0]][o[1]])
        print(currentState,goalState[0])

        if currentState == goalState[0]:
            path = backtrace(parent, startState, currentState)
            pathTraversed += path
            print("This", pathTraversed, noOfStatesVisited)
            return pathTraversed, noOfStatesVisited

        #print(currentState)
        openSet.remove(currentState)
        visited.append(currentState)
        #print(openSet)
        noOfStatesVisited += 1
        neighbors = maze.getNeighbors(currentState[0], currentState[1])
        for nbr in neighbors:
            if nbr in visited:
                continue
            else:
                h[nbr[0]][nbr[1]] = manhattan(nbr, goalState[0])
                parent[nbr] = currentState
                openSet.add(nbr)






def astar(maze):
    # TODO: Write your code here
    pathsVert= {}
    distances = {}
    noSV = {}
    verticeEdg = {}
    distList =[]
    goalState = maze.getObjectives()
    startState = maze.getStart()
    #goalState.append(startState)

    minValue = 1000000
    minPath = 0
    minNSV = 0
    print(len(goalState))
    for i in goalState:
        print(i)
        if i != (64,55):
            path, value, nsv = astarSub(maze, startState, i)
            if minValue > value:
                minValue = value
                minPath = path
                minNSV = nsv
    return(minPath, minNSV)

    # for i in goalState:
    #     for j in goalState:
    #         if i != j:
    #             path, value, nsv = astarSub(maze, i, j)
    #             distances[(i, j)] = value
    #             pathsVert[(i, j)] = path
    #             noSV[(i, j)] = nsv
    #             distList.append(value)


    pt, sv = astarFinal(maze, startState, goalState, distances, distList, pathsVert, noSV)
    #print("HERERE")
    return pt, sv

    #return [],0


def find(parnt, i):
    if parnt[i] == i:
        return i
    return find(parnt, parnt[i])

def union( parnt, rank, x, y):
    xroot = find(parnt, x)
    yroot = find(parnt, y)

    # Attach smaller rank tree under root of
# high rank tree (Union by Rank)
    if rank[xroot] < rank[yroot]:
        parnt[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parnt[yroot] = xroot

    # If ranks are same, then make one as root
    # and increment its rank by one
    else:
        parnt[yroot] = xroot
        rank[xroot] += 1

def kruskalMST (distances, goalsList):
    result = []
    goalIndex = {}
    e = 0
    i = 0
    parnt =[]
    rank = []
    numVert = len(goalsList)
    sumOfWt = 0

    for node in range(numVert):
        goalIndex[goalsList[node]] = node
        parnt.append(node)
        rank.append(0)

    while e

        minEdge = distances[min(distances.keys(), key=(lambda k: distances[k]))]
        #print(len(distances))
        for key in distances:
            #print(distances[key], minEdge)< (numVert - 1):
            if distances[key] == minEdge:
                u, v = key
                keyD = (v, u)
                distances.pop(key)
                #print(len(distances))
                #print("dist", distances[v, u])
                distances.pop(keyD)
                #print(len(distances))
                #print(u, v, "NextRound")
                break

        x = find(parnt, goalIndex[u])
        y = find(parnt, goalIndex[v])

        if x != y:
            e = e+1
            sumOfWt += minEdge
            union(parnt, rank, goalIndex[u], goalIndex[v])
    #print(" Ks DONEEEE! ")
    return(sumOfWt)

def astarFinal (maze, startState, goalsList, distances, distList, pathVert, noSV):
    openSet = set()
    closedSet = set()
    (row, col) = maze.getDimensions()
    g = [[0 for i in range(col)] for j in range(row)]
    h = [[0 for i in range(col)] for j in range(row)]
    pathTraversed = []
    pathTraversed.append(startState)
    noOfStatesVisited = 1
    parent = {}
    openSet.add(startState)
    distRef = distances.copy()
    #print("SS", startState)
    while openSet:

        for i in openSet:
            print("UPAR", i, g[i[0]][i[1]] + h[i[0]][i[1]])
        distCopy = distances.copy()
        currentState = min(openSet, key=lambda o: g[o[0]][o[1]] + h[o[0]][o[1]])
        #print("CS :", currentState, closedSet, openSet, noOfStatesVisited, goalsList)
        #print("distt", distances)
        heurestic = kruskalMST(distances, goalsList)
        distances = distCopy.copy()
        #print("back", currentState, heurestic, closedSet, openSet, noOfStatesVisited)
        goalsList.remove(currentState)
        openSet.remove(currentState)
        lastVert = pathTraversed[-1]
        print("lastVErt: ", lastVert, currentState, openSet, heurestic)
        if closedSet:
            pathTraversed.remove(lastVert)
            if parent[currentState] != lastVert:
                key = (lastVert, parent[currentState])
                pathTraversed += pathVert[key]
                noOfStatesVisited += noSV[key]
                pathTraversed.remove(pathTraversed[-1])
                key = (parent[currentState], currentState)
                pathTraversed += pathVert[key]
                noOfStatesVisited += noSV[key]
            else:
                key = (lastVert, currentState)
                pathTraversed += pathVert[key]
                noOfStatesVisited += noSV[key]

        if goalsList == []:
            #path = pathback(parent, startState, currentState, pathVert)
            #pathTraversed += path
            return pathTraversed, noOfStatesVisited

        #noOfStatesVisited += 1
        #print("CS", currentState)
        #print("clo", closedSet)
        closedSet.add(currentState)
        #print("cur:", currentState)
        neighbors = goalsList

        #print("OS", openSet)
        #print("cs", closedSet)
        #print("curr", currentState)
        #print("neigh", neighbors)
        #print(len(distances))
        for nbr in neighbors:

            if nbr in closedSet:
                #newG = g[currentState[0]][currentState[1]] + distances[currentState, nbr] + heurestic
                #if g[nbr[0]][nbr[1]] + h[nbr[0]][nbr[1]] > newG:
                    #g[nbr[0]][nbr[1]] = g[currentState[0]][currentState[1]] + distances[currentState, nbr]
                    #h[nbr[0]][nbr[1]] = heurestic
                    #parent[nbr] = currentState
                    #closedSet.remove(nbr)
                    #openSet.add(nbr)
                #else:
                continue
            if nbr in openSet:

                newG = (g[currentState[0]][currentState[1]] + distances[currentState, nbr]) + heurestic
                print( nbr, newG)
                if g[nbr[0]][nbr[1]] + h[nbr[0]][nbr[1]] + distRef[currentState, parent[nbr]] > newG:
                    print("HERE")
                    g[nbr[0]][nbr[1]] = g[currentState[0]][currentState[1]] + distances[currentState, nbr]
                    h[nbr[0]][nbr[1]] = heurestic
                    print("aft", g[nbr[0]][nbr[1]] + h[nbr[0]][nbr[1]])
                    parent[nbr] = currentState
                else:
                    g[nbr[0]][nbr[1]] += distRef[currentState, parent[nbr]]



            else:

                g[nbr[0]][nbr[1]] = g[currentState[0]][currentState[1]] + distances[currentState, nbr]
                h[nbr[0]][nbr[1]] = heurestic
                print(nbr, g[nbr[0]][nbr[1]] + h[nbr[0]][nbr[1]] )
                parent[nbr] = currentState
                openSet.add(nbr)
        #print("am i here?")


        #print("d2", len(distances))

        for key in distCopy:
            u, v = key
            if u == currentState or v == currentState:
                distances.pop(key)

        #print("d3", len(distances))



def astarSub(maze, startState, goalState):
    #print("HERE")
    openSet = set()
    closedSet = set()
    (row, col) = maze.getDimensions()
    g = [[0 for i in range(col)] for j in range(row)]
    h = [[0 for i in range(col)] for j in range(row)]
    pathTraversed = []
    noOfStatesVisited = 1
    parent = {}


    openSet.add(startState)

    while openSet:
        currentState = min(openSet, key=lambda o: g[o[0]][o[1]] + h[o[0]][o[1]])

        if currentState == goalState:
           print("HERe")
           path = backtrace(parent, startState, currentState)
           pathTraversed += path
           return pathTraversed, (len(pathTraversed) - 1), noOfStatesVisited


        openSet.remove(currentState)
        noOfStatesVisited += 1
        closedSet.add(currentState)
        neighbors = maze.getNeighbors(currentState[0], currentState[1])
        for nbr in neighbors:
            if nbr in closedSet:
                newG = g[currentState[0]][currentState[1]] + 1
                if g[nbr[0]][nbr[1]] > newG:
                    g[nbr[0]][nbr[1]] = newG
                    parent[nbr] = currentState
                    closedSet.remove(nbr)
                    openSet.add(nbr)
                else:
                    continue
            if nbr in openSet:
                newG = g[currentState[0]][currentState[1]] + 1
                if g[nbr[0]][nbr[1]] > newG:
                    g[nbr[0]][nbr[1]] = newG
                    parent[nbr] = currentState
            else:
                g[nbr[0]][nbr[1]] = g[currentState[0]][currentState[1]] + 1
                h[nbr[0]][nbr[1]] = manhattan(nbr, goalState)
                parent[nbr] = currentState
                openSet.add(nbr)





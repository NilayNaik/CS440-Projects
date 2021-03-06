# code implementation of strategy 1
from Preliminaries import DFS, AStar
from Preliminaries import mazeGenerator
# very simple algo: just use A* to get a path and then move agent along the path while incrementing fire
# fire generation included in algo

# returns position died in
def doStrategyOne(maze,flammabilityRate):
    mazeGenerator.initializeFire(maze)
    # path given by A*
    path = AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))

    for step in path:
        # first step logic
        if step[0]==0 and step[1]==0:
            # then we just move the agent and continue
            maze[step[0]][step[1]] = 2
            continue
        # we just move agent and then increment the fire
        # because we used bfs, we cannot possibly hit an obstacle, but we might hit fire and die
        if maze[step[0]][step[1]]==-1:
            # return the failed pos
            return step
        else:
            # then we move the agent and increment the fire
            maze[step[0]][step[1]]=2
            if step == (len(maze)-1,len(maze)-1):
                # agent Survived!
                break
            mazeGenerator.lightMaze(maze,flammabilityRate)
            # checking if fire is on the step we just moved to
            if maze[step[0]][step[1]]==-1:
                return step
    # if we reached the end we can just return the last point
    return (len(maze)-1,len(maze)-1)


# Same as doStrategyOne but if given a maze already on fire (for use in probability helper)
def doStrategyOneForHelper(maze,flammabilityRate):
    # path given by A*
    aStarPath = AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))

    for step in aStarPath:
        # first step logic
        if step[0]==0 and step[1]==0:
            # then we just move the agent and continue
            maze[step[0]][step[1]] = 2
            continue
        # we just move agent and then increment the fire
        # because we used bfs, we cannot possibly hit an obstacle, but we might hit fire and die
        if maze[step[0]][step[1]] == -1:
            # return the failed pos
            return step
        else:
            # then we move the agent and increment the fire
            maze[step[0]][step[1]]=2
            mazeGenerator.lightMaze(maze,flammabilityRate)
            # checking if fire is on the step we just moved to
            if maze[step[0]][step[1]] == -1:
                return step
    # if we reached the end we can just return the last point
    return (len(maze)-1,len(maze)-1)


# returns a list of tuples corresponding to each obstacle density incremented by 0.05
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def strategyOneProbabilityHelper(dim,sampleSize):
    #inputOutput is our list of tuples
    goal = (dim - 1, dim - 1)
    inputOutput=[]
    desiredDensity = 0.3
    currFlammability = 0.0
    while currFlammability <= 1:
        strategyOneSuccessCount = 0
        for i in range(sampleSize):

            # generating maze
            maze = mazeGenerator.generateMaze(dim, desiredDensity)
            fireLoc = mazeGenerator.initializeFire(maze)
            # Generate mazes and fire until there is a path from agent to goal and from agent to the fire
            while not (DFS.dfs(maze, (0,0), goal) and DFS.dfs(maze, (0,0), fireLoc)):
                maze = mazeGenerator.generateMaze(dim, desiredDensity)
                fireLoc = mazeGenerator.initializeFire(maze)
            print("fire: ", fireLoc)
            endingLoc = doStrategyOneForHelper(maze, currFlammability)
            print("Loc: ", endingLoc)
            if endingLoc == goal:
                strategyOneSuccessCount += 1
                print("success")
            print("fin trial", i+1)
        print("flammability:", currFlammability)
        # now we have the probability for this flammability
        probability = strategyOneSuccessCount/sampleSize
        inputOutput.append((currFlammability,probability))
        currFlammability = round(currFlammability + 0.05, 2)
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput

# gradual printing of strategy 1 on a maze on fire
def printStrategyOneStep(maze, flammabilityRate, path):
    if path is None:
        mazeGenerator.initializeFire(maze)
        path =AStar.aStarGetPath(maze,(0,0),(len(maze)-1,len(maze)-1))
        locToMove = path.popleft()
        maze[locToMove[0]][locToMove[1]]=2
        return True,path
    else:
        locToMove=path.popleft()
        if maze[locToMove[0]][locToMove[1]]==-1:
            # agent burns
            return False,path
        # moving agent
        maze[locToMove[0]][locToMove[1]]=2
        # generating fire
        litSpots=mazeGenerator.lightMaze(maze,flammabilityRate)
        if locToMove in litSpots:
            # agent burned up
            return False,path
        if locToMove ==(len(maze)-1,len(maze)-1):
            return False,path
        else:
            return True,path


def printStrategyOne(maze,flammabilityRate):
    path=None
    while True:
        result = printStrategyOneStep(maze,flammabilityRate,path)
        path=result[1]
        mazeGenerator.printMaze(maze)
        if not result[0]:
            break
    # printing final state
    mazeGenerator.printMaze(maze)

def printEntireStrategyOne(maze,flammabilityRate):
    doStrategyOne(maze,flammabilityRate)
    mazeGenerator.printMaze(maze)

# code implementation of strategy 2
# recalculating A* at each step
from Preliminaries import mazeGenerator, DFS, AStar

def doStrategyTwo(maze,flammabilityRate):
   # initialize random starting point for fire
   mazeGenerator.initializeFire(maze)
   currPosition=(0,0)
   maze[0][0]=2

   while True:
      #first spot is the start, so we pick the next one
      path=AStar.aStarGetPath(maze,currPosition,(len(maze)-1,len(maze)-1))
      currLoc=path.popleft()
      if not path:
          # then no place to move to (no path found)
          return currLoc
      posToPick=path.popleft()

      if maze[posToPick[0]][posToPick[1]]==-1:
         # return this pos because the agent will burn here
         return posToPick

      # checking goal status
      if posToPick == (len(maze) - 1, len(maze) - 1):
        # then the agent has found his way to the goal
        maze[posToPick[0]][posToPick[1]] = 2
        return posToPick
      else:
         # then we move agent here and advance fire
         currPosition=posToPick
         maze[currPosition[0]][currPosition[1]]=2
         mazeGenerator.lightMaze(maze,flammabilityRate)
         # checking if the spot is on fire now
         if maze[currPosition[0]][currPosition[1]]==-1:
            # returning the position because the agent will burn
            return currPosition

# Same as doStrategyTwo but given a maze already on fire (for use in probability helper)
def doStrategyTwoForHelper(maze,flammabilityRate):
   currPosition = (0,0)

   while True:
      #first spot is the start, so we pick the next one
      path = AStar.aStarGetPath(maze, currPosition, (len(maze)-1,len(maze)-1))
      if len(path) > 1:
         posToPick = path[1]
      else:
         return currPosition
      #checking goal status
      if posToPick==(len(maze)-1,len(maze)-1):
         # then the agent has found his way to the goal
         maze[posToPick[0]][posToPick[1]]=2
         return posToPick

      if maze[posToPick[0]][posToPick[1]]==-1:
         # return this pos because the agent will burn here
         return posToPick
      else:
         # then we move agent here and advance fire
         currPosition = posToPick
         maze[currPosition[0]][currPosition[1]]=2
         mazeGenerator.lightMaze(maze,flammabilityRate)
         # checking if the spot is on fire now
         if maze[currPosition[0]][currPosition[1]]==-1:
            # returning the position because the agent will burn
            return currPosition

# returns a list of tuples corresponding to each obstacle density incremented by 0.05
# sample size is the number of times to run the test for each blocking density
# dim is the dimension of the maze to use for probability helper
def strategyTwoProbabilityHelper(dim,sampleSize):
    #inputOutput is our list of tuples
    goal = (dim - 1, dim - 1)
    inputOutput=[]
    desiredDensity = 0.3
    currFlammability = 0.0
    while currFlammability <= 1:
        strategyTwoSuccessCount = 0
        for i in range(sampleSize):
            
            # generating maze
            maze = mazeGenerator.generateMaze(dim, desiredDensity)
            fireLoc = mazeGenerator.initializeFire(maze)
            # Generate mazes and fire until there is a path from agent to goal and from agent to the fire
            while not (DFS.dfs(maze, (0,0), goal) and DFS.dfs(maze, (0,0), fireLoc)):
                maze = mazeGenerator.generateMaze(dim, desiredDensity)
                fireLoc = mazeGenerator.initializeFire(maze)
            print("fire: ", fireLoc)
            endingLoc = doStrategyTwoForHelper(maze, currFlammability)
            print("Loc: ", endingLoc)
            if endingLoc == goal:
                strategyTwoSuccessCount += 1
                print("success")
            print("fin trial", i+1)
        print("flammability:", currFlammability)
        # now we have the probability for this flammability
        probability = strategyTwoSuccessCount/sampleSize
        inputOutput.append((currFlammability,probability))
        currFlammability = round(currFlammability + 0.05, 2)
    # returning our list of tuples to use with mathplotlib for plotting a graph

    return inputOutput


# gradual printing of strategy 2 on a maze on fire
# recalculating at each step
def printStrategyTwoStep(maze,flammabilityRate,loc):
    if loc==(0,0):
        # need to initialize fire
        mazeGenerator.initializeFire(maze)
        maze[0][0]=2
    path = AStar.aStarGetPath(maze,loc,(len(maze)-1,len(maze)-1))
    # popping already taken path
    currLoc =path.popleft()
    if not path:
        # then no more valid path
        return False,currLoc
    # getting new spot to move to
    locToMove = path.popleft()
    if maze[locToMove[0]][locToMove[1]] == -1:
        # agent burns
        return False,locToMove
    # moving agent
    maze[locToMove[0]][locToMove[1]] = 2
    # checking goal
    if locToMove == (len(maze) - 1, len(maze) - 1):
        return False,locToMove
    # generating fire
    litSpots = mazeGenerator.lightMaze(maze, flammabilityRate)
    if maze[locToMove[0]][locToMove[1]]==-1:
        # agent burned up
        return False,locToMove
    else:
        return True,locToMove


def printStrategyTwo(maze,flammabilityRate):
    loc=(0,0)
    result = printStrategyTwoStep(maze,flammabilityRate,loc)
    loc=result[1]
    mazeGenerator.printMaze(maze)
    while result[0]:
        result=printStrategyTwoStep(maze,flammabilityRate,loc)
        loc=result[1]
        mazeGenerator.printMaze(maze)
    mazeGenerator.printMaze(maze)

def printEntireStrategyTwo(maze,flammabilityRate):
    doStrategyTwo(maze,flammabilityRate)
    mazeGenerator.printMaze(maze)



from Board import *
from Belief import *
from Agent import *

basicOneTotal = 0
basicTwoTotal = 0
advancedTotal = 0

dim = 50
numMaps = 10
numTrials = 10

for i in range(numMaps):

    print("Next Map: ", i+1)

    # Generate a new map.
    testBoard = Board(dim)
    testBoard.generateTerrain()

    testBoard.printBoard()
    print()
    # testBoard.printColoredBoard()

    # Randomize starting location for the agents for each map
    randX = random.randint(0, dim - 1)
    randY = random.randint(0, dim - 1)
    randomStart = (randX, randY)

    for j in range(numTrials):

        print("Next Trial: ", j+1)

        print("target at: ", testBoard.getTarget(), "with terrain: ", testBoard.getTerrainType(testBoard.getTarget()), " agent start: ", randomStart)

        agentBelief = Belief(testBoard)

        # agentBelief.printBelief()

        # Run each agent and print running totals (not averages) as they are completed.

        basicOneTotal += basicAgentOne(testBoard, agentBelief, randomStart)
        print("Basic Agent One completed")
        print("basic one: ", basicOneTotal)

        agentBelief2 = Belief(testBoard)

        basicTwoTotal += basicAgentTwo(testBoard, agentBelief2, randomStart)
        print("Basic Agent Two completed")
        print("basic two: ", basicTwoTotal)

        agentBelief3 = Belief(testBoard)

        advancedTotal += advancedAgent(testBoard, agentBelief3, randomStart)
        print("Advanced Agent completed")
        print("advanced: ", advancedTotal)


# Print the total steps taken (not an average)
print("basic one: ", basicOneTotal)
print("basic two: ", basicTwoTotal)
print("advanced: ", advancedTotal)



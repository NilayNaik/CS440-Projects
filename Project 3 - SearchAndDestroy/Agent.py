
import random
from Board import *

# Basic Agent One Implementation, searches based on highest P(Target in cell)
def basicAgentOne(board, belief, initial):
    # Initializes the starting location of the Agent
    randX = random.randint(0, board.getDimension() - 1)
    randY = random.randint(0, board.getDimension() - 1)
    currentLocation = (randX, randY)
    currentLocation = initial

    targetFound = False
    searchCount = 0
    totalDistanceTraveled = 0

    # While the target has not been found, go to the next cell to search, search, and update beliefs accordingly.
    while not targetFound:
        distanceTraveledToNextSearch = 0
        nextSearch =  belief.getNextHighestBeliefContainingTarget(currentLocation)
        while currentLocation != nextSearch:
            if currentLocation[0] < nextSearch[0]:
                currentLocation = (currentLocation[0] + 1, currentLocation[1])
            elif currentLocation[0] > nextSearch[0]:
                currentLocation = (currentLocation[0] -1, currentLocation[1])
            elif currentLocation[1] < nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] + 1)
            elif currentLocation[1] > nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] - 1)
            distanceTraveledToNextSearch += 1            

        totalDistanceTraveled += distanceTraveledToNextSearch

        targetFound = board.searchCell(nextSearch)
        searchCount += 1
        belief.updateBelief(nextSearch)

        # print("Current Loc: ", currentLocation)
        # belief.printBelief()
        
    return searchCount + totalDistanceTraveled
        
# Basic Agent Two Implementation, searches based on highest P(Target in cell) * P(successful search))
def basicAgentTwo(board, belief, initial):
    # Initializes the starting location of the Agent
    randX = random.randint(0, board.getDimension() - 1)
    randY = random.randint(0, board.getDimension() - 1)
    currentLocation = (randX, randY)
    currentLocation = initial

    targetFound = False
    searchCount = 0
    totalDistanceTraveled = 0

    # While the target has not been found, go to the next cell to search, search, and update beliefs accordingly.
    while not targetFound:
        distanceTraveledToNextSearch = 0
        nextSearch =  belief.getNextHighestBeliefFindingTarget(currentLocation)
        while currentLocation != nextSearch:
            if currentLocation[0] < nextSearch[0]:
                currentLocation = (currentLocation[0] + 1, currentLocation[1])
            elif currentLocation[0] > nextSearch[0]:
                currentLocation = (currentLocation[0] -1, currentLocation[1])
            elif currentLocation[1] < nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] + 1)
            elif currentLocation[1] > nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] - 1)
            distanceTraveledToNextSearch += 1

        totalDistanceTraveled += distanceTraveledToNextSearch

        targetFound = board.searchCell(nextSearch)
        searchCount += 1
        belief.updateBelief(nextSearch)

        # print("Current Loc: ", currentLocation)
        # belief.printBelief()

    return searchCount + totalDistanceTraveled
        
# Advanced Agent Implementation, searches based on highest P(Target in cell) * P(successful search) / 2
def advancedAgent(board, belief, initial):
    # Initializes the starting location of the Agent
    randX = random.randint(0, board.getDimension() - 1)
    randY = random.randint(0, board.getDimension() - 1)
    currentLocation = (randX, randY)
    currentLocation = initial

    targetFound = False
    searchCount = 0
    totalDistanceTraveled = 0

    # While the target has not been found, go to the next cell to search, search, and update beliefs accordingly.
    while not targetFound:
        distanceTraveledToNextSearch = 0
        nextSearch =  belief.getNextHighestBeliefAdvanced(currentLocation)
        while currentLocation != nextSearch:
            if currentLocation[0] < nextSearch[0]:
                currentLocation = (currentLocation[0] + 1, currentLocation[1])
            elif currentLocation[0] > nextSearch[0]:
                currentLocation = (currentLocation[0] -1, currentLocation[1])
            elif currentLocation[1] < nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] + 1)
            elif currentLocation[1] > nextSearch[1]:
                currentLocation = (currentLocation[0], currentLocation[1] - 1)
            distanceTraveledToNextSearch += 1

        totalDistanceTraveled += distanceTraveledToNextSearch

        targetFound = board.searchCell(nextSearch)
        searchCount += 1
        belief.updateBelief(nextSearch)

        # print("Current Loc: ", currentLocation)
        # belief.printBelief()

    return searchCount + totalDistanceTraveled
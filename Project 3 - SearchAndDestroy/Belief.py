
import random

# Represents the beliefs for the location of the target on the board.
class Belief():
    def __init__(self, board):
        # Initialize the initial beliefs for each coordinate containing the target P(target in cell) to be equally likely.
        self.beliefs = {}
        self.board = board
        self.dim = board.getDimension()
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                self.beliefs[(i,j)] = 1 / (self.dim * self.dim)

    # Updates the beliefs for the target location for every cell.
    def updateBelief(self, searchedCell):
        # Use Bayes Theorem to update beliefs of every cell

        # P(Target NOT found | Target in Cell)
        if searchedCell in self.board.flatTerrain:
            falseNegativeRate = 0.1
        elif searchedCell in self.board.hillyTerrain:
            falseNegativeRate = 0.3
        elif searchedCell in self.board.forestedTerrain:
            falseNegativeRate = 0.7
        elif searchedCell in self.board.caveTerrain:
            falseNegativeRate = 0.9

        # Update belief for searched cell
        probabilityContainsTarget = self.beliefs[searchedCell]
        self.beliefs[searchedCell] = (probabilityContainsTarget * falseNegativeRate) / ((1 - probabilityContainsTarget) + (probabilityContainsTarget * falseNegativeRate))

        # Update belief for all other cells
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                if (i,j) != searchedCell:
                    # Prior belief that target is in a cell (P(Target in cell))
                    priorBeliefTargetInCell = self.beliefs[(i,j)]

                    # Probability for a successful search given target is in a cell.
                    successRate = 1 - falseNegativeRate

                    # Posterior beliefs for other cells
                    self.beliefs[(i,j)] = priorBeliefTargetInCell * ( 1 / (1 - (probabilityContainsTarget * successRate)) )


    # Returns the next cell to be searched based on highest likelihood of CONTAINING the target (for Basic Agent 1).
    def getNextHighestBeliefContainingTarget(self, currentLocation):

        # Gets the cells of the board and sorts them in order of decreasing belief. Then from the most probable options, sorts them by distance and keeps the closest ones.
        beliefList = []
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                beliefList.append((i,j))
        beliefList.sort(reverse = True, key = lambda n : self.beliefs[n])
        nextToSearch = beliefList[0]
        filter(self.beliefs[nextToSearch], beliefList)
        beliefList.sort(reverse = True, key = lambda loc : self.board.getManhattanDistance(loc, currentLocation))
        nextToSearch = beliefList[0]
        filter(self.board.getManhattanDistance(nextToSearch, currentLocation), beliefList)

        randNeighborIndex = random.randint(0, len(beliefList) - 1)
        nextToSearch = beliefList[randNeighborIndex]

        return nextToSearch

    # Returns the next cell to be searched based on highest likelihood of FINDING the target (for Basic Agent 2).
    def getNextHighestBeliefFindingTarget(self, currentLocation):

        # Gets the cells of the board and sorts them in order of decreasing belief * successRate. Then from the most probable options, sorts them by distance and keeps the closest ones.
        beliefList = []
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                beliefList.append((i,j))
        beliefList.sort(reverse = True, key = lambda n : (self.beliefs[n] * self.board.getTerrainSuccessRate(n)))
        nextToSearch = beliefList[0]
        filter(self.beliefs[nextToSearch], beliefList)
        beliefList.sort(reverse = True, key = lambda loc : self.board.getManhattanDistance(loc, currentLocation))
        nextToSearch = beliefList[0]
        filter(self.board.getManhattanDistance(nextToSearch, currentLocation), beliefList)

        randNeighborIndex = random.randint(0, len(beliefList) - 1)
        nextToSearch = beliefList[randNeighborIndex]

        return nextToSearch

    # Returns the next cell to be searched based on highest likelihood of FINDING the target (weighted) (for Advanced Agent).
    def getNextHighestBeliefAdvanced(self, currentLocation):        

        # Gets the cells of the board and sorts them in order of decreasing belief * successRate / 2. Then from the most probable options, sorts them by distance and keeps the closest ones.
        beliefList = []
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                beliefList.append((i,j))
        beliefList.sort(reverse = True, key = lambda n : (self.beliefs[n] * self.board.getTerrainSuccessRate(n) / 2))
        nextToSearch = beliefList[0]
        filter(self.beliefs[nextToSearch], beliefList)
        beliefList.sort(reverse = True, key = lambda loc : self.board.getManhattanDistance(loc, currentLocation))
        nextToSearch = beliefList[0]
        filter(self.board.getManhattanDistance(nextToSearch, currentLocation), beliefList)

        randNeighborIndex = random.randint(0, len(beliefList) - 1)
        nextToSearch = beliefList[randNeighborIndex]

        return nextToSearch

    # Prints the current beliefs for the location of the target.
    def printBelief(self):
        for i in range(0, self.dim):
            for j in range(0, self.dim):
                print(self.beliefs[(i,j)], end="")
            print()

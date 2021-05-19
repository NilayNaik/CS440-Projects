
import random


# Represents the board containing the target to be searched for.
class Board():
    def __init__(self, dim):
        # Set Board Dimension
        self.dim = dim
        # Set Target Location
        randX = random.randint(0, self.dim - 1)
        randY = random.randint(0, self.dim - 1)
        self.target = (randX, randY)
        # Sets of tuple coordinates for each terrain type
        self.flatTerrain = set()
        self.hillyTerrain = set()
        self.forestedTerrain = set()
        self.caveTerrain = set()
    
    # Generates the terrain for each location on the Board.
    def generateTerrain(self):
        for i in range(self.dim):
            for j in range(self.dim):
                # Randomly choose terrain type for a cell
                terrainChoice = random.randint(1,4)
                # 1:Flat terrain, 2:Hilly terrain, 3:Forested terrain, 4:Cave terrain
                if terrainChoice == 1:
                    self.flatTerrain.add((i,j))
                elif terrainChoice == 2:
                    self.hillyTerrain.add((i,j))
                elif terrainChoice == 3:
                    self.forestedTerrain.add((i,j))
                elif terrainChoice == 4:
                    self.caveTerrain.add((i,j))

    # Searches a cell and returns whether the target was found.
    def searchCell(self, cellToSearch):
        # If target is in the cell being searched
        if cellToSearch == self.target:
            # Proabability of search being successful given target is in the cell P(found target | target in cell).
            successProbability = random.randint(1, 10)
            if cellToSearch in self.flatTerrain:
                if successProbability > 1:
                    return True
            elif cellToSearch in self.hillyTerrain:
                if successProbability > 3:
                    return True
            elif cellToSearch in self.forestedTerrain:
                if successProbability > 7:
                    return True
            elif cellToSearch in self.caveTerrain:
                if successProbability > 9:
                    return True
        # Otherwise, target was not found in the search or target is not in the cell
        return False

    # Randomize target location
    def relocateTarget(self):
        randX = random.randint(0, self.dim-1)
        randY = random.randint(0, self.dim-1)
        self.target = (randX, randY)

    # Returns the manhattan distance between two cells.
    def getManhattanDistance(self, loc1, loc2):
        return abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])

    # Returns the valid neighbors of a given location (that is neighbors immediately up/down/left/right within the board dimensions).
    def getValidNeighbors(self, loc):
        neighbors = []
        neighbors.append((loc[0] - 1, loc[1]))           # neighbor above
        neighbors.append((loc[0], loc[1] + 1))           # neighbor right
        neighbors.append((loc[0] + 1, loc[1]))           # neighbor below
        neighbors.append((loc[0], loc[1] - 1))           # neighbor left
        validNeighbors = []
        for neighbor in neighbors:
            if neighbor[0] >= 0 and neighbor[0] < self.dim and neighbor[1] >= 0 and neighbor[1] < self.dim:
                validNeighbors.append(neighbor)

        return validNeighbors

    # Returns the dimension of the board.
    def getDimension(self):
        return self.dim

    # Returns the target location.
    def getTarget(self):
        return self.target
    
    # Returns the terrain type of the requested cell (as an integer)
    # 1:Flat terrain, 2:Hilly terrain, 3:Forested terrain, 4:Cave terrain
    def getTerrainType(self, loc):
        if loc in self.flatTerrain:
            return 1
        elif loc in self.hillyTerrain:
            return 2
        elif loc in self.forestedTerrain:
            return 3
        elif loc in self.caveTerrain:
            return 4

    # Returns the probability for successfully finding the target in a cell (given the target is in the cell).
    def getTerrainSuccessRate(self, loc):
            if loc in self.flatTerrain:
                return 1 - 0.1
            elif loc in self.hillyTerrain:
                return 1 - 0.3
            elif loc in self.forestedTerrain:
                return 1 - 0.7
            elif loc in self.caveTerrain:
                return 1 - 0.9

    # Prints the Board with designated terrain values.
    # 1:Flat terrain, 2:Hilly terrain, 3:Forested terrain, 4:Cave terrain
    def printBoard(self):
            for i in range(self.dim):
                for j in range(self.dim):
                    if (i,j) in self.flatTerrain:
                        print(" 1 ", end="")
                    elif (i,j) in self.hillyTerrain:
                        print(" 2 ", end="")
                    elif (i,j) in self.forestedTerrain:
                        print (" 3 ", end="")
                    elif (i,j) in self.caveTerrain:
                        print(" 4 ", end="")
                print()

    # Prints the Board with color-coded terrain. (Works below dimension size 30)
    def printColoredBoard(self):
        flatTerrainColor = '\033[31m'
        hillyTerrainColor = '\033[93m'
        forestedTerrainColor = '\033[32m'
        caveTerrainColor = '\033[90m'
        defaultColor = '\033[37m'
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) in self.flatTerrain:
                    print(f"{flatTerrainColor} 1 ", end="")
                elif (i,j) in self.hillyTerrain:
                    print(f"{hillyTerrainColor} 2 ", end="")
                elif (i,j) in self.forestedTerrain:
                    print (f"{forestedTerrainColor} 3 ", end="")
                elif (i,j) in self.caveTerrain:
                    print(f"{caveTerrainColor} 4 ", end="")
            print(f"{defaultColor}")
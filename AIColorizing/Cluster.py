import random

# Do k-Means Clustering to find the most representative colors in the image.
# Returns a tuple of the centers (as RGB colors) and a dictionary of the pixels for each center.
def makeClusters(pixelList):
    # Select numClusters centers at random
    setOfRGBCenters = set()
    numClusters = 5
    while (len(setOfRGBCenters) != numClusters):
        randIndex = random.randint(0, len(pixelList) - 1)
        setOfRGBCenters.add(pixelList[randIndex][1])

    newCenterSet = set()

    # Repeat center calculations until they no longer change.
    while setOfRGBCenters != newCenterSet:


        if newCenterSet != set():
            setOfRGBCenters = newCenterSet

        dictCenters = {}
        for kCenter in setOfRGBCenters:
            dictCenters[kCenter] = []

        # Adds pixels to the closest center.
        # pixel in form ( (x,y),(r,g,b) )
        for pixel in pixelList:
            closestCenter = getClosestCenter(pixel, setOfRGBCenters)
            dictCenters[closestCenter].append(pixel)

        # Recalculates the centers.
        newCenterSet = set()
        for center in setOfRGBCenters:
            sumR = 0
            sumG = 0
            sumB = 0
            pixelCount = 0
            for pixel in dictCenters[center]:
                sumR += pixel[1][0]
                sumG += pixel[1][1]
                sumB += pixel[1][2]
                pixelCount += 1

            averageRGB = center
            if pixelCount != 0:
                averageRGB = (round(sumR / pixelCount), round(sumG / pixelCount), round(sumB / pixelCount))
            newCenterSet.add(averageRGB)

    return (setOfRGBCenters, dictCenters)

# Returns the closest cluster center for a given pixel from a set of centers.
def getClosestCenter(pixel, setOfRGBCenters):
    centerDistances = []
    for center in setOfRGBCenters:
        centerDistances.append((center, getManhattanColorDistance(pixel[1], center)))
    centerDistances.sort(key = lambda n : n[1])
    return centerDistances[0][0]

# Numerical representation of distance from one color to another.
def getManhattanColorDistance(col1, col2):
    return abs(col2[0] - col1[0]) + abs(col2[1] - col1[1]) + abs(col2[2] - col1[2])

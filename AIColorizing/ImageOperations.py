
from PIL import Image
from Cluster import *
import math


# Creates a grayscale version of an image and saves it.
# Takes in an image file name and returns the name of the new grayscale image
def createGrayscale(imageFile):
    image = Image.open(imageFile)
    pixels = image.load()
    (width, height) = image.size
    for i in range(width):
        for j in range(height):
            gray = 0.21 * pixels[i,j][0] + 0.72 * pixels[i,j][1] + 0.07 * pixels[i,j][2]
            gray = round(gray)
            pixels[i,j] = (gray, gray, gray)
    image.save("grayscale_" + imageFile)
    image.close()
    return "grayscale_" + imageFile

# Open and displays an image.
# Takes in an image file name and returns nothing.
def showImage(imageFile):
    image = Image.open(imageFile)
    image.show()
    image.close()

# Splits an image into two halves (left/right) and saves them as separate files (training/testing).
# Takes in an image file name and returns nothing.
def splitImage(imageFile):
    image = Image.open(imageFile)
    (width, height) = image.size
    leftHalf = (0, 0, width/2, height)
    rightHalf = (width/2, 0, width, height)
    trainingHalf = image.crop(leftHalf)
    testingHalf = image.crop(rightHalf)
    trainingHalf.save("trainingHalf.jpg")
    testingHalf.save("testingHalf.jpg")
    image.close()
    return ("trainingHalf.jpg", "testingHalf.jpg")

# Given an image, saves and returns the recolored image using representative colors from k-means clustering.
# Also saves each cluster color to its own file. Returns the recolored image.
def recolorImage(imageFile):
    image = Image.open(imageFile)
    pixels = image.load()
    (width, height) = image.size

    # Recolors and saves an image to a new file using the representative colors from k-means clustering.
    pixelList = []
    for i in range(width):
        for j in range(height):
            pixelList.append(((i,j), (pixels[i,j][0], pixels[i,j][1], pixels[i,j][2]))) 

    clusterResult = makeClusters(pixelList)
    kColors = clusterResult[0]
    colorDict = clusterResult[1]
    for k in kColors:
        for pixel in colorDict[k]:
            pixels[pixel[0][0], pixel[0][1]] = (k[0], k[1], k[2])
    image.save("recolored_" + imageFile)

    # Saves the representative colors as separate files for reference.
    kCount = 0
    for k in kColors:
        kCount += 1
        for i in range(width):
            for j in range(height):
                color = k
                pixels[i,j] = (color[0], color[1], color[2])
        image.save("colorK_" + str(kCount) + imageFile)

    image.close()
    return "recolored_" + imageFile


# Returns a list of the total value of the colors in a patch for each patch center.
def findPatchColorTotals(image):
    imagePixels = image.load()
    (imageWidth, imageHeight) = image.size
    patchColorTotals = []
    for i in range(1, imageWidth - 1):
        for j in range(1, imageHeight - 1):
            totalR = imagePixels[i-1,j-1][0] + imagePixels[i-1,j][0] + imagePixels[i-1,j+1][0] + imagePixels[i,j-1][0] + imagePixels[i,j][0] + imagePixels[i,j+1][0] + imagePixels[i+1,j-1][0] + imagePixels[i+1,j][0] + imagePixels[i+1,j+1][0]
            totalG = imagePixels[i-1,j-1][1] + imagePixels[i-1,j][1] + imagePixels[i-1,j+1][1] + imagePixels[i,j-1][1] + imagePixels[i,j][1] + imagePixels[i,j+1][1] + imagePixels[i+1,j-1][1] + imagePixels[i+1,j][1] + imagePixels[i+1,j+1][1]
            totalB = imagePixels[i-1,j-1][2] + imagePixels[i-1,j][2] + imagePixels[i-1,j+1][2] + imagePixels[i,j-1][2] + imagePixels[i,j][2] + imagePixels[i,j+1][2] + imagePixels[i+1,j-1][2] + imagePixels[i+1,j][2] + imagePixels[i+1,j+1][2]
            patchColorTotals.append(((i,j), (totalR, totalG, totalB)))
    return patchColorTotals

# Returns the numPatches most similar patch centers for some list of colors and some main patch.
def findSimilarPatches(patchColorTotals, mainPatch, numPatches):
    similarPatches = []
    possiblePatches = []
    mainPatchR = 0
    mainPatchG = 0
    mainPatchB = 0
    
    # Finds the total color value for the main patch.
    for i in range(len(mainPatch[0])):
        for j in range(len(mainPatch)):
            mainPatchR += mainPatch[i][j][1][0]
            mainPatchG += mainPatch[i][j][1][1]
            mainPatchB += mainPatch[i][j][1][2]
    mainPatchColor = (mainPatchR, mainPatchG, mainPatchB)

    # Creates a list of tuples containing patch centers and their color differences (as a value) with the main patch.
    for tup in patchColorTotals:
        patchCenter = tup[0]
        color = tup[1]
        colorSquareTotal = (color[0]*9, color[1]*9, color[2]*9)
        possiblePatches.append((patchCenter, getManhattanColorDistance(colorSquareTotal, mainPatchColor)))

    possiblePatches.sort(key = lambda n : n[1])

    for i in range(numPatches):
        similarPatches.append(possiblePatches[i][0])

    return similarPatches

# Gets the color of the given location in the colored training data corresponding to the gray image.
def getPatchCenterColor(patchCenter):

    colorTraining = Image.open("trainingHalf.jpg")
    colorPixels = colorTraining.load()
    centerColor = colorPixels[patchCenter[0], patchCenter[1]]
    colorTraining.close()
    return centerColor


# Returns the numPatches most similar patch centers for some list of colors (adjusted with sigmoid) and some main patch.
def findSimilarPatchesSigmoid(patchColorTotals, mainPatch, numPatches):
    similarPatches = []
    possiblePatches = []
    mainPatchR = 0
    mainPatchG = 0
    mainPatchB = 0
    
    # Finds the total color value for the main patch.
    for i in range(len(mainPatch[0])):
        for j in range(len(mainPatch)):
            mainPatchR += mainPatch[i][j][1][0]
            mainPatchG += mainPatch[i][j][1][1]
            mainPatchB += mainPatch[i][j][1][2]
    mainPatchColor = (mainPatchR / 255, mainPatchG / 255, mainPatchB / 255)

    # Creates a list of tuples containing patch centers and their color differences (as a value) with the main patch.
    for tup in patchColorTotals:
        patchCenter = tup[0]
        color = tup[1]
        colorSquareTotal = ( sigmoid(round(color[0]*9 / 255)), sigmoid(round(color[1]*9 / 255)), sigmoid(round(color[2]*9 / 255)))
        possiblePatches.append((patchCenter, getManhattanColorDistance(colorSquareTotal, mainPatchColor)))

    possiblePatches.sort(key = lambda n : n[1])

    for i in range(numPatches):
        similarPatches.append(possiblePatches[i][0])

    return similarPatches

def sigmoid(x):
    return (1 / (1 + math.exp(-x)))*255


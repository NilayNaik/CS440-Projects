
from PIL import Image
from ImageOperations import *

from Cluster import *

from collections import Counter


# Initialize images and training/testing sets.

imageFile = "spongebob.jpg"

image = Image.open(imageFile)

imageHalves = splitImage(imageFile)
grayImage = createGrayscale(imageFile)
grayTrainingHalf = createGrayscale(imageHalves[0])
grayTestingHalf = createGrayscale(imageHalves[1])

image = Image.open(imageFile)
pixels = image.load()
(width, height) = image.size

pixelList = []

for i in range(width):
    for j in range(height):
        pixelList.append(((i,j), (pixels[i,j][0], pixels[i,j][1], pixels[i,j][2]))) 

recoloredImage = recolorImage(imageFile)
imageHalves = splitImage(recoloredImage)
image.close()

# Iterate through every 3x3 patch in the testing set and use the training set to choose a suitable color for each patch center.

trainImage = Image.open(grayTrainingHalf)
trainPixels = trainImage.load()
(trainWidth, trainHeight) = trainImage.size

trainColorImage = Image.open(imageHalves[0])
trainColorPixels = trainColorImage.load()
(trainColorWidth, trainColorHeight) = trainColorImage.size

testImage = Image.open(grayTestingHalf)
testPixels = testImage.load()
(testWidth, testHeight) = testImage.size

similarTestPatch = []

# A list of total color values for every 3x3 square
patchColorTotals = findPatchColorTotals(trainImage)
testPatchColorTotals = findPatchColorTotals(testImage)


# Basic Agent
for i in range(1, testWidth - 1):
    for j in range(1, testHeight - 1):
        
        possibleColors = []

        patchToColor = [[((i-1,j-1),(testPixels[i-1,j-1])), ((i-1,j),(testPixels[i-1,j])), ((i-1,j+1),(testPixels[i-1,j+1]))],
                        [((i,j-1),(testPixels[i,j-1])), ((i,j),(testPixels[i,j])), ((i,j+1),(testPixels[i,j+1]))],
                        [((i+1,j-1),(testPixels[i+1,j-1])), ((i+1,j),(testPixels[i+1,j])), ((i+1,j+1),(testPixels[i+1,j+1]))]]

        similarPatches = findSimilarPatches(patchColorTotals, patchToColor, 6)
        for patch in similarPatches:
            possibleColors.append(getPatchCenterColor(patch))

        mostCommonColor = Counter(possibleColors).most_common(2)

        inferredColor = mostCommonColor[0][0]
        # if len(mostCommonColor) > 1:
        #     if (mostCommonColor[0][1] == mostCommonColor[1][1]):
        #         similarTestPatch = findSimilarPatches(testPatchColorTotals, patchToColor, 1)[0]
        #         inferredColor = getPatchCenterColor(similarTestPatch)


        testPixels[i,j] = inferredColor

testImage.save("restoredColor_" + imageFile)

restoredImage = Image.open("restoredColor_" + imageFile)

mergedImage = Image.new('RGB', (trainColorImage.width + restoredImage.width, trainColorImage.height))
mergedImage.paste(trainColorImage, (0, 0))
mergedImage.paste(restoredImage, (trainColorImage.width, 0))

mergedImage.save("mergedImage_" + imageFile)

mergedImage.show()

# Advanced Agent
# for i in range(1, testWidth - 1):
#     for j in range(1, testHeight - 1):
        
#         possibleColors = []

#         patchToColor = [[((i-1,j-1),(testPixels[i-1,j-1])), ((i-1,j),(testPixels[i-1,j])), ((i-1,j+1),(testPixels[i-1,j+1]))],
#                         [((i,j-1),(testPixels[i,j-1])), ((i,j),(testPixels[i,j])), ((i,j+1),(testPixels[i,j+1]))],
#                         [((i+1,j-1),(testPixels[i+1,j-1])), ((i+1,j),(testPixels[i+1,j])), ((i+1,j+1),(testPixels[i+1,j+1]))]]

#         similarPatches = findSimilarPatchesSigmoid(patchColorTotals, patchToColor, 6)
#         for patch in similarPatches:
#             possibleColors.append(getPatchCenterColor(patch))

#         mostCommonColor = Counter(possibleColors).most_common(2)

#         inferredColor = mostCommonColor[0][0]
#         # if len(mostCommonColor) > 1:
#         #     if (mostCommonColor[0][1] == mostCommonColor[1][1]):
#         #         similarTestPatch = findSimilarPatches(testPatchColorTotals, patchToColor, 1)[0]
#         #         inferredColor = getPatchCenterColor(similarTestPatch)


#         testPixels[i,j] = inferredColor

# testImage.save("restoredColorAdv_" + imageFile)

# restoredImage = Image.open("restoredColorAdv_" + imageFile)

# mergedImage = Image.new('RGB', (trainColorImage.width + restoredImage.width, trainColorImage.height))
# mergedImage.paste(trainColorImage, (0, 0))
# mergedImage.paste(restoredImage, (trainColorImage.width, 0))

# mergedImage.save("mergedImageAdv_" + imageFile)

# mergedImage.show()


trainImage.close()
trainColorImage.close()
testImage.close()

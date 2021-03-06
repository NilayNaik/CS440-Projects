# this serves as a driver to generate a plot for A* using matplotlib

# calls the A* probability helper function and uses it to generate a plot

from Preliminaries.AStar import aStarProbabilityHelper
import matplotlib.pyplot as plt

# will increment blocking factor from 0.05 to 1 in steps of 0.05, then it will generate a maze of size mazeDimension
    # then it will run the preliminary A* implementation
    # this is repeated sampleSize times for every new matrix to get a solid probability
    # the results are outputted in an array of tuples in the form [(blockingFactor,averageNodesExplored),...]
    # these results will make the graph easy to plot and we will have a solid number of points of data

mazeDimension = 500
sampleSize = 20
result = aStarProbabilityHelper(mazeDimension, sampleSize)

# now performing matplotlib logic to generate the graph
#including data points

plt.scatter(*zip(*result))
plt.plot(*zip(*result))
plt.title(f"Average Number of Nodes Explored via A* vs Blocking Factor (on maze of size {mazeDimension})")
plt.xlabel("Blocking Factor")
plt.ylabel(f"Average Number of Nodes Explored (from {sampleSize} trials)")
plt.xticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
# plt.yticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.show()
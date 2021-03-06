# This serves as a driver to generate a plot for Strategy1 using matplotlib

# calls strategy1 probability helper function and uses it to generate a plot

from Strategies import Strategy1
import matplotlib.pyplot as plt

# will increment blocking factor from 0.05 to 1 in steps of 0.05, then it will generate a maze of dim 100
    # then it will run the strategy1 implementation
    # this is repeated 20 times for every new matrix to get a solid probability
    # the results are outputted in an array of tuples in the form [(flammabilityRate,probSuccess),...]
    # these results will make the graph easy to plot and we will have a solid number of points of data
    # All mazes will have a blocking factor p = 0.3

result = Strategy1.strategyOneProbabilityHelper(100,20)
# now performing matplotlib logic to generate the graph


#including data points

plt.scatter(*zip(*result))
plt.plot(*zip(*result))
plt.title("Probability of Success via Strategy1 vs Flammability Rate (on maze of size 100)")
plt.xlabel("Flammability rate")
plt.ylabel("Probability of success (from 20 trials per increment)")
plt.xticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.yticks([0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])
plt.ylim(ymin=0)
plt.xlim(xmin=0)
plt.grid()
plt.show()
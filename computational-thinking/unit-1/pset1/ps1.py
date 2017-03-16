###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    """
    Maggie,3
    Herman,7
    Betsy,9
    Oreo,6
    Moo Moo,3
    Milkshake,2
    Millie,5
    Lola,2
    Florence,2
    Henrietta,9
    """
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """

    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    copyCows = [(k, cows[k]) for k in sorted(cows, key=cows.get, reverse=True)]

    trips = [[[], 0]]
    
    for name, value in copyCows:    

        for newTrip in trips:
            if newTrip[1] + value <= limit:
                newTrip[0].append(name)
                newTrip[1] += value
                break
        else:
            if value <= limit:
                trips.append([[], 0])
                trips[-1][0].append(name)
                trips[-1][1] += value
            
    return [trip[0] for trip in trips]

def greedy_cow_transport(cows,limit=10):
        
    copyCows = [(k, cows[k]) for k in sorted(cows, key=cows.get, reverse=True)]
    
    result = []
    used = []
    cowsNum = len(copyCows)
    while len(used) != cowsNum:
        
        currentTrip = []
        currentValue = 0
        for name, value in copyCows:
            if name in used:
                continue;
            elif value > limit:
                used.append(name)
            elif currentValue + value <= limit:
                currentTrip.append(name)
                used.append(name)
                currentValue += value
        else:
            result.append(currentTrip)
            
    return result

# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    minimalCount = 0
    bestForNow  = []

    for cowPowerSet in get_partitions(cows):
        for combination in cowPowerSet:
            combinationValue = 0;
            for singleCow in combination:
                combinationValue += cows[singleCow]
            if combinationValue > limit:
                break;
        else:
            if minimalCount == 0:
                minimalCount = len(cowPowerSet)
            if len(cowPowerSet) <= minimalCount:
                minimalCount = len(cowPowerSet)
                bestForNow = cowPowerSet

    return bestForNow

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    limit=10
    print(cows)
    start = time.time()
    print(greedy_cow_transport(cows, limit))
    middle = time.time()
    print(brute_force_cow_transport(cows, limit))
    end = time.time()
    
    print(end - middle, middle - start)


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

# cows = load_cows("ps1_cow_data.txt")
# limit=10
# print(cows)

# print(greedy_cow_transport(cows, limit))
# print(brute_force_cow_transport(cows, limit))
compare_cow_transport_algorithms()
import numpy as np
import math 

class Node:
    def __init__(self):
        return

def decision_tree_learning(training_dataset, depth):
    labelCol = 7
    numOfRows = len(training_dataset)
    numOfCols = len(training_dataset[0])
    firstLabel = training_dataset[0][labelCol]

    # Check if all samples have the same label 
    for row in range(numOfRows):
        if training_dataset[row][labelCol] != firstLabel:
            # return (a leaf node with this value, depth)
            break

    # Split if all samples do not have the same label
    splitAttribute, splitValue = find_split(training_dataset)
    print splitAttribute, splitValue

    return

# Return the attribute and the value that results in the maximum information gain
def find_split(training_dataset):
    maxInformationGain = 0.0
    splitAttribute = 0
    splitValue = 0
    labelCol = 7
    numOfRows = len(training_dataset)
    numOfAttributes = len(training_dataset[0]) - 1

    for attribute in range(numOfAttributes):
        sortedCopy = training_dataset[np.argsort(training_dataset[:, attribute])] # sort by attribute
        currentLabel = sortedCopy[0][labelCol]
        for row in range(numOfRows):
            if sortedCopy[row][labelCol] != currentLabel:
                sLeft = sortedCopy[0:row - 1, :]
                sRight = sortedCopy[row:, :]
                informationGain = calculate_gain(sortedCopy, sLeft, sRight)
                if informationGain > maxInformationGain:
                    maxInformationGain = informationGain
                    splitAttribute = attribute
                    splitValue = sortedCopy[row - 1][attribute]
                currentLabel = sortedCopy[row][labelCol]

    return (splitAttribute, splitValue)

# Calculate information gain associated with particular split
def calculate_gain(sAll, sLeft, sRight):
    h_sAll = calculate_entropy(sAll)
    remainder = calculate_remainder(sLeft, sRight)

    return h_sAll - remainder

# Calculate entropy (H value)
def calculate_entropy(dataset):
    labelCol = 7
    numOfRows = len(dataset)
    pDictionary = {}

    # Iterate through the dataset and update the pDictionary
    for row in range(numOfRows):
        key = dataset[row][labelCol]
        if key in pDictionary:
            pDictionary[key] += 1
        else:
            pDictionary[key] = 1

    # Convert the absolute values in pDictionary into proportions
    for key in pDictionary:
        pDictionary[key] = float(pDictionary[key]) / numOfRows    

    # Perform the summation to calculate entropy
    entropy = 0.0
    for key in pDictionary:
        entropy += pDictionary[key] * math.log(pDictionary[key], 2)

    return -entropy

# Calculate remainder
def calculate_remainder(sLeft, sRight):
    sLeftLength = len(sLeft)
    sRightLength = len(sRight)
    sum = sLeftLength + sRightLength

    return (sLeftLength / sum) * (calculate_entropy(sLeft)) + (sRightLength / sum) * (calculate_entropy(sRight))

if __name__ == "__main__":
    cleanDataset = np.loadtxt("clean_dataset.txt")
    depth = 0
    decision_tree_learning(cleanDataset, depth)
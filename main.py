import numpy as np
import math 

class Node:
    def __init__(self, splitAttribute, splitValue, terminalValue, depth):
        self.splitAttribute = splitAttribute
        self.splitValue = splitValue
        self.terminalValue = terminalValue
        self.depth = depth
        self.left = None
        self.right = None
        print(splitAttribute, splitValue, terminalValue, depth)

    def insert(self, leftBranch, rightBranch):
        self.left = leftBranch
        self.right = rightBranch

# Main function to recursively train the decision tree
def decision_tree_learning(training_dataset, depth):
    numOfRows = len(training_dataset)
    numOfCols = len(training_dataset[0])

    if numOfRows == 1:
        return (Node(None, None, training_dataset[0, -1], depth), depth)

    # Check if all samples have the same label 
    for row in range(1, numOfRows):
        if training_dataset[row, -1] != training_dataset[row - 1, -1]:
            break
        elif row == numOfRows - 1:
            return (Node(None, None, training_dataset[0, -1], depth), depth)

    # Split if all samples do not have the same label
    splitAttribute, splitValue, leftDataset, rightDataset = find_split(training_dataset)

    # Create a new root node using the split
    root = Node(splitAttribute, splitValue, None, depth)

    # Recursively generate nodes for left and right branches of the root node and insert them
    leftBranch, leftDepth = decision_tree_learning(leftDataset, depth + 1)
    rightBranch, rightDepth = decision_tree_learning(rightDataset, depth + 1)
    root.insert(leftBranch, rightBranch)

    # Return the root node
    return (root, max(leftDepth, rightDepth))

# Find and return the attribute and the value that results in the maximum information gain
# Also return the dataset that is split according to the attribute and value found
def find_split(training_dataset):
    maxInformationGain = 0.0
    splitAttribute = 0
    splitValue = 0
    indexOfSplit = 0
    leftDataset = None
    rightDataset = None
    numOfRows = len(training_dataset)
    numOfAttributes = len(training_dataset[0]) - 1

    for attribute in range(numOfAttributes):
        sortedCopy = training_dataset[np.argsort(training_dataset[:, attribute])] # sort by attribute
        for row in range(1, numOfRows):
            if sortedCopy[row - 1, -1] != sortedCopy[row, -1]:
                sLeft = sortedCopy[0:row, -1]
                sRight = sortedCopy[row:, -1]
                informationGain = calculate_gain(sortedCopy[:, -1], sLeft, sRight)
                if informationGain > maxInformationGain:
                    maxInformationGain = informationGain
                    splitAttribute = attribute
                    splitValue = (sortedCopy[row - 1, attribute] + sortedCopy[row, attribute]) / 2
                    leftDataset = sortedCopy[0:row, :]
                    rightDataset = sortedCopy[row:, :]       
    
    return (splitAttribute, splitValue, leftDataset, rightDataset)

# Calculate information gain associated with particular split
def calculate_gain(sAll, sLeft, sRight):
    h_sAll = calculate_entropy(sAll)
    remainder = calculate_remainder(sLeft, sRight)

    return h_sAll - remainder

# Calculate entropy (H value)
def calculate_entropy(dataset):
    numOfRows = len(dataset)
    pDictionary = {}

    # Iterate through the dataset and update the pDictionary
    for row in range(numOfRows):
        key = dataset[row]
        if key in pDictionary:
            pDictionary[key] += 1
        else:
            pDictionary[key] = 1

    # Convert the absolute values in pDictionary into proportions
    for key in pDictionary:
        pDictionary[key] = float(pDictionary[key]) / numOfRows

    # Perform the summation to calculate entropy
    entropy = 0.000
    for key in pDictionary:
        entropy += pDictionary[key] * np.log2(pDictionary[key])

    return -entropy

# Calculate remainder
def calculate_remainder(sLeft, sRight):
    sLeftLength = len(sLeft)
    sRightLength = len(sRight)
    sum = sLeftLength + sRightLength

    return (sLeftLength / sum) * (calculate_entropy(sLeft)) + (sRightLength / sum) * (calculate_entropy(sRight))

if __name__ == "__main__":
    dataset = np.loadtxt("clean_dataset.txt")
    depth = 0
    decision_tree_learning(dataset, depth)
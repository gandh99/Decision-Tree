######################################################################################
#                                                                                    #
# File Description: Evaluates a decision tree given an already-trained decision tree #
#                                                                                    #
######################################################################################

from train_model import *

# Evaluate accuracy of decision tree using a confusion matrix
# Store the results in a label dictionary
def evaluate(testDB, trainedTree):
    index = 0
    totalErrors = 0
    numOfRows = len(testDB)
    confusionMatrix = create_confusion_matrix(4, 4)
    labelDict = dict.fromkeys({"label1", "label2", "label3", "label4"})

    # Generate the confusion matrix
    for row in range(numOfRows):
        classify(testDB[row, :], trainedTree, confusionMatrix)

    # Compute and store the metrics 
    for element in labelDict:
        truePositive, falsePositive, falseNegative = calculate_metrics(confusionMatrix, index)
        recall = calculate_recall(truePositive, falseNegative)
        precision = calculate_precision(truePositive, falsePositive)
        f1 = calculate_f1(recall, precision)
        totalErrors += falsePositive

        labelDict[element] = {"recall": recall, "precision": precision, "f1": f1}
        index += 1

    accuracy = calculate_classification_rate(numOfRows, totalErrors)
    for element in labelDict:
        print(element, ":", labelDict[element])
    print("Accuracy:", accuracy)

    return 

# Classify a particular data point
def classify(data, node, confusionMatrix):
    while (node.terminalValue == None):
        if data[node.splitAttribute] < node.splitValue:
            node = node.left
        else:
            node = node.right

    expectedIndex = int(data[-1]) - 1
    predictedIndex = int(node.terminalValue) - 1
    confusionMatrix[predictedIndex, expectedIndex] += 1

# Create confusion matrix (predicted x expected)
def create_confusion_matrix(numOfRows, numOfColumns):
    matrix = np.zeros(shape = (numOfRows, numOfColumns))

    return matrix

# Metric: true positive, false positive, false negative
def calculate_metrics(matrix, index):
    numOfRows = len(matrix)
    truePositive = matrix[index, index]
    falsePositive = 0
    falseNegative = 0

    # Calculate false positive and false negative
    for currentIndex in range(numOfRows):
        if currentIndex == index:
            continue
        falsePositive += matrix[index, currentIndex]
        falseNegative += matrix[currentIndex, index]    

    return truePositive, falsePositive, falseNegative

# Metric: recall = true pos / (true pos + false neg)
def calculate_recall(truePositive, falseNegative):
    return truePositive / (truePositive + falseNegative)

# Metric: precision = true pos / (true pos + false pos)
def calculate_precision(truePositive, falsePositive):
    return truePositive / (truePositive + falsePositive)

# Metric: F1 = 2 * (prec * rec) / (prec + rec)
def calculate_f1(precision, recall):
    return 2 * (precision * recall) / (precision + recall)

# Metric: classification rate = 1 - classification error
def calculate_classification_rate(numOfRows, totalErrors):
    return (numOfRows - totalErrors) / numOfRows
    

if __name__ == "__main__":
    trainingDataset = np.loadtxt("clean_dataset.txt")
    # np.random.shuffle(trainingDataset)    # Optional: Shuffle dataset
    depth = 0
    root, depth = decision_tree_learning(trainingDataset, depth)
    evaluate(trainingDataset, root)


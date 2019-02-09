############################################################################################
#                                                                                    	   #
# File Description: Performs 10-fold cross-validation on both the clean and noisy datasets #
#                                                                                    	   #
############################################################################################

from train_model import *
from evaluate_model import *
from prune_model import *
from plot_model import *
import sys

# Perform k-fold cross-validation on the dataset in the specified file
# First set aside the test dataset. The rest of the dataset will then be used for training and validation
def cross_validate(filename, kFold = 10, prune = False, plotTree = False):
	dataset = np.loadtxt(filename)
	segmentSize = int(dataset.shape[0] / kFold)
	depth = 0

	# Store the metrics from each k-fold iteration in a list to be used for computing the average at the end
	listOfAccuracy = []
	listOfConfusionMatrix = []
	listOfLabelDict = []

	# First shuffle the dataset
	np.random.shuffle(dataset)

	# If pruning, set aside 10% of the data for testing and 90% of the data for training and validation
	if prune:
		testingDataset = dataset[0:segmentSize, :]
		trainingAndValidationDataset = dataset[segmentSize:, :]
	# If not pruning, we will not use a separate testing set. Instead, we will use the validation set to evaluate the tree
	else:
		trainingAndValidationDataset = dataset

	# Perform k-fold cross-validation to generate a set of metrics on the performance of the tree
	for k in range(kFold):
		print("Processing fold no.: ", k + 1)	# Fold counting starts from 1	
		segmentSize = int(trainingAndValidationDataset.shape[0] / kFold)

	    # Split dataset into discrete training and validation sets
		validationDataset = trainingAndValidationDataset[k*segmentSize:(k + 1)*segmentSize, :]
		trainingDataset1 = trainingAndValidationDataset[0:k*segmentSize, :]
		trainingDataset2 = trainingAndValidationDataset[(k + 1)*segmentSize:, :]
		trainingDataset = np.concatenate((trainingDataset1, trainingDataset2))
		
		# Train the dataset
		depth = 0
		root, depth = decision_tree_learning(trainingDataset, depth)

		# Evaluate the tree. Prune the tree first if prune was set to True 
		if prune:
			originalAccuracy, confusionMatrix, labelDict = evaluate(validationDataset, root)		
			root = prune_tree(root, originalAccuracy, validationDataset)
			testAccuracy, testConfusionMatrix, testLabelDict = evaluate(testingDataset, root)
		else:
			testAccuracy, testConfusionMatrix, testLabelDict = evaluate(validationDataset, root)

		# Store the evaluation results into their appropriate list
		listOfAccuracy.append(testAccuracy)
		listOfConfusionMatrix.append(testConfusionMatrix)
		listOfLabelDict.append(testLabelDict)

		# Plot the tree (only for the last k) if plotTree was set to True
		if plotTree and k == kFold - 1:
			plot_tree(root)

	# Compute the averages of the metrics that were previously stored in a list
	averageAccuracy, averageConfusionMatrix, averageLabelDict = calculate_metric_average(listOfAccuracy, listOfConfusionMatrix, listOfLabelDict)

	# Optional: Print results of the average metrics
	print("Average Confusion Matrix:\n", averageConfusionMatrix)
	print("\nAverage Statistics for individual labels:")
	for element in averageLabelDict:
		print(element, ":", averageLabelDict[element])
	print("\nAverage Accuracy on test set:", averageAccuracy)

# Takes in the lists of metrics and computes their averages
def calculate_metric_average(listOfAccuracy, listOfConfusionMatrix, listOfLabelDict):
	# Calculate average accuracy
	averageAccuracy = 0
	for accuracy in listOfAccuracy:
		averageAccuracy += accuracy
	averageAccuracy /= len(listOfAccuracy)

	# Calculate average confusion matrix
	averageConfusionMatrix = np.zeros(shape = listOfConfusionMatrix[0].shape)
	for matrix in listOfConfusionMatrix:
		averageConfusionMatrix += matrix
	averageConfusionMatrix /= len(listOfConfusionMatrix)

	# Calculate average label dictionary
	averageLabelDict = dict.fromkeys({"label1", "label2", "label3", "label4"})
	numOfDict = len(listOfLabelDict)
	for label in averageLabelDict:
		averageLabelDict[label] = {"recall": 0.000, "precision": 0.000, "f1": 0.000} 
	for labelDict in listOfLabelDict:
		for key in averageLabelDict:
			averageLabelDict[key]["recall"] += labelDict[key]["recall"] / numOfDict
			averageLabelDict[key]["precision"] += labelDict[key]["precision"] /numOfDict
			averageLabelDict[key]["f1"] += labelDict[key]["f1"] / numOfDict

	return averageAccuracy, averageConfusionMatrix, averageLabelDict

# Simple function to convert a string to its boolean form
def string_to_bool(string):
	if string == "True":
		return True
	elif string == "False":
		return False
	else:
		print("argument for boolean: <True/False>")
		raise ValueError


if __name__ == "__main__":
	if (len(sys.argv) == 5):
		filename = sys.argv[1]
		kFold = int(sys.argv[2])
		prune = string_to_bool(sys.argv[3])
		plotTree = string_to_bool(sys.argv[4])
		cross_validate(filename, kFold, prune, plotTree)
	else:
		print("usage: <filename> <kFold> <prune: True/False> <plotTree: True/False>")

	# # Emergency use if command line does not work
	# filename = "noisy_dataset.txt"
	# kFold = 10
	# prune = True
	# plotTree = True
	# cross_validate(filename, kFold, prune, plotTree)


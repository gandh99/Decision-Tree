############################################################################################
#                                                                                    	   #
# File Description: Performs 10-fold cross-validation on both the clean and noisy datasets #
#                                                                                    	   #
############################################################################################

from train_model import *
from evaluate_model import *
from prune_model import *

# Perform k-fold cross-validation on the dataset in the specified file
# First set aside the test dataset. The rest of the dataset will then be used for training and validation
def cross_validate(filename, kFold = 10):
	dataset = np.loadtxt(filename)
	segmentSize = int(dataset.shape[0] / kFold)
	depth = 0

	# Store the metrics from each k-fold iteration in a list to be used for computing the average at the end
	listOfAccuracy = []
	listOfConfusionMatrix = []
	listOfLabelDict = []

	# First shuffle the dataset
	np.random.shuffle(dataset)

	# Set aside 10% of data to be the test dataset used at the end. 
	# The rest (90%) of the data will be used for training and validation
	testingDataset = dataset[0:segmentSize, :]
	trainingAndValidationDataset = dataset[segmentSize:, :]

	# Perform k-fold cross-validation to determine the decision tree that performs best on the validation set
	for k in range(kFold):		
		segmentSize = int(len(trainingAndValidationDataset) / kFold)

	    # Split dataset into discrete training and validation sets
		validationDataset = trainingAndValidationDataset[k*segmentSize:(k + 1)*segmentSize, :]
		trainingDataset1 = trainingAndValidationDataset[0:k*segmentSize, :]
		trainingDataset2 = trainingAndValidationDataset[(k + 1)*segmentSize:, :]
		trainingDataset = np.concatenate((trainingDataset1, trainingDataset2))

		# Train the dataset
		root, depth = decision_tree_learning(trainingDataset, depth)

		# Prune the decision tree
		originalAccuracy, confusionMatrix, labelDict = evaluate(validationDataset, root)		
		root = prune_tree(root, originalAccuracy, validationDataset)

		# Evaluate the trained decision tree using the appropriate dataset store the metrics in a list
		testAccuracy, testConfusionMatrix, testLabelDict = evaluate(validationDataset, root)
		listOfAccuracy.append(testAccuracy)
		listOfConfusionMatrix.append(testConfusionMatrix)
		listOfLabelDict.append(testLabelDict)

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


if __name__ == "__main__":
	cross_validate("noisy_dataset.txt", 10)


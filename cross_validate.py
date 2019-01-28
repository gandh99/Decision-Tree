############################################################################################
#                                                                                    	   #
# File Description: Performs 10-fold cross-validation on both the clean and noisy datasets #
#                                                                                    	   #
############################################################################################

from train_model import *
from evaluate_model import *

# Perform k-fold cross-validation on the dataset in the specified file
# First set aside the test dataset. The rest of the dataset will then be used for training and validation
# The best-performing training set will be used as the decision tree for testing on the test dataset
def cross_validate(filename, kFold = 10):
	dataset = np.loadtxt(filename)
	segmentSize = int(len(dataset) / kFold)
	depth = 0
	highestAccuracy = 0.000
	bestTree = None

	# First shuffle the dataset
	np.random.shuffle(dataset)

	# Set aside 10% of data to be the test dataset used at the end. 
	# The rest (90%) of the data will be used for training and validation
	testingDataset = dataset[0:segmentSize, :]
	trainingAndValidationDataset = dataset[segmentSize:, :]

	# Perform k-fold cross-validation to determine the training set that performs best on the validation set
	for k in range(kFold):
		segmentSize = int(len(trainingAndValidationDataset) / kFold)

	    # Split dataset into discrete training and validation sets
		validationDataset = trainingAndValidationDataset[k*segmentSize:(k + 1)*segmentSize, :]
		trainingDataset1 = trainingAndValidationDataset[0:k*segmentSize, :]
		trainingDataset2 = trainingAndValidationDataset[(k + 1)*segmentSize:, :]
		trainingDataset = np.concatenate((trainingDataset1, trainingDataset2))

		# Train the dataset
		root, depth = decision_tree_learning(trainingDataset, depth)

		# Evaluate the trained decision tree using the validation dataset and select the best tree
		accuracy, confusionMatrix, labelDict = evaluate(validationDataset, root)
		if accuracy > highestAccuracy:
			bestTree = root

	# Use the best decision tree from the k-fold cross-validation to test on the test dataset
	testAccuracy, confusionMatrix, labelDict = evaluate(testingDataset, bestTree)

	# Optional: Print results
	print("Confusion Matrix:\n", confusionMatrix)
	print("\nStatistics for individual labels:")
	for element in labelDict:
		print(element, ":", labelDict[element])
	print("\nAccuracy:", testAccuracy)


if __name__ == "__main__":
	cross_validate("noisy_dataset.txt", 10)


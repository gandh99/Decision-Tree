############################################################################################
#                                                                                    	   #
# File Description: Performs 10-fold cross-validation on both the clean and noisy datasets #
#                                                                                    	   #
############################################################################################

from train_model import *
from evaluate_model import *

if __name__ == "__main__":
	dataset = np.loadtxt("clean_dataset.txt")
	# dataset = np.loadtxt("noisy_dataset.txt")
	kFold = 10
	segmentSize = int(len(dataset) / 10)
	depth = 0

	# First shuffle the dataset
	np.random.shuffle(dataset)

	# Perform k-fold cross-validation to generate a series of metrics for each iteration
	for k in range(kFold):
	    # Split dataset into discrete training and testing sets
		testingDataset = dataset[k*segmentSize:(k + 1)*segmentSize, :]
		trainingDataset1 = dataset[0:k*segmentSize, :]
		trainingDataset2 = dataset[(k + 1)*segmentSize:, :]
		trainingDataset = np.concatenate((trainingDataset1, trainingDataset2))

		# Train the dataset
		root, depth = decision_tree_learning(trainingDataset, depth)

		# Evaluate the dataset
		evaluate(testingDataset, root)

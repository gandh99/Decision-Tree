############################################################################################
#                                                                                    	   #
# File Description: Performs 10-fold cross-validation on both the clean and noisy datasets #
#                                                                                    	   #
############################################################################################

from train_model import *
from evaluate_model import *


if __name__ == "__main__":
    trainingDataset = np.loadtxt("clean_dataset.txt")
    depth = 0
    root, depth = decision_tree_learning(trainingDataset, depth)

    testingDataset = np.loadtxt("noisy_dataset.txt")
    evaluate(testingDataset, root)
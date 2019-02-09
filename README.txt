1. Introduction
This README describes the relevant APIs that can be used, as well as how the code should be run.
Skip directly to Section 3 in order to quickly get started with the code.
The code comprises 4 different files: 
	- train_model.py
	- evaluate_model.py
	- prune_model.py
	- cross_validate.py

1.1. Environment Setup
- python3.7.2
- Numpy
- Matplotlib

2. Files and APIs

2.1. train_model.py
- decision_tree_learning(training_dataset, depth): 
	- training_dataset: NumPy array of the training dataset
	- depth: Integer
	- [return]: Root of trained decision tree (Node object) and depth of tree

2.2. evaluate_model.py
- evaluate(testDB, trainedTree): 
	- testDB: NumPy array of the test dataset
	- trainedTree: Root of trained decision tree (Node object)
	- [return]: 
		- accuracy: Average classification rate
		- confusionMatrix: 4x4 NumPy array representing (predicted x expected) labels
		- labelDict: Dictionary with keys = {label1, label2, label3 and label4}. Value is a dictionary with keys = {recall, precision, f1}

2.3. prune_model.py
- prune_tree(root, originalAccuracy, validationDataset):
	- root: Root of trained decision tree (Node object)
	- originalAccuracy: Accuracy of trained tree before pruning, evaluated on the validation dataset
	- validationDataset: NumPy array of the validation dataset
	- [return]: Root of pruned decision tree (Node object)

2.4. cross_validate.py
- cross_validate(filename, kFold, prune, plotTree):
	- filename: Name of the file on which to perform cross validation
	- kFold: Number of times to perform the k-fold cross validation. Default = 10
	- prune: Boolean variable on whether to prune the decision tree. Default = False
	- [output]: 
		- Average accuracy
		- Average confusion matrix
		- Average values for labelDict

2.5. plot_model.py
- plot_tree(node):
	- node: Root of trained decision tree (Node object)
	- [output]:
		- Visualisation of the tree in matplotlib


3. How to use the code
Option 1: Run from command line (Windows):
		- python .\cross_validate.py <filename> <kFold> <prune: True/False> <plotTree: True/False>
	  Run from command line (Linux/macOS):
		- python cross_validate.py <filename> <kFold> <prune: True/False> <plotTree: True/False>
Option 2: Manually edit the source code in the cross_validate.py file. 
	  In the __main__ section, you may modify any of the following in the cross_validate function:
	- filename
	- kFold
	- prune
	- plotTree
Output:
	- Be patient and the results (metric averages of all folds) will then be printed onto the screen. 






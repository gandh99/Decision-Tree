##########################################################################
#                                                                        #
# File Description: Prunes a decision tree that has already been trained #
#                                                                        #
##########################################################################

from train_model import *
from evaluate_model import *

# Main function to prune the decision tree and then return the pruned tree
def prune_tree(root, originalAccuracy, validationDataset):
	# print("Number of nodes (before pruning):", root.get_number_of_nodes())	#DELETE
	# print("Accuracy (before pruning):", originalAccuracy)	#DELETE
	currentAccuracy = [originalAccuracy]
	while True:
		nodesToPrune = [False]
		traverse_tree(root, root, nodesToPrune, currentAccuracy, validationDataset)		
		# print("Number of nodes (after pruning):", root.get_number_of_nodes())		#DELETE
		# print("Accuracy (after pruning):", (evaluate(validationDataset, root))[0])	#DELETE

		if nodesToPrune[0] == False:
			# print("Number of nodes (after pruning):", root.get_number_of_nodes())		#DELETE
			return root

# Traverse the tree looking for nodes connected to 2 leaves and then attempt to prune them
def traverse_tree(root, node, nodesToPrune, currentAccuracy, validationDataset):
	# Return if the node is a leaf
	if node.terminalValue != None:
		return
	# If the node is connected to 2 leaves, attempt to prune it
	elif node.left.terminalValue != None and node.right.terminalValue != None:
		prune_node(root, node, nodesToPrune, currentAccuracy, validationDataset)
		return
	# Otherwise continue traversing the tree to look for nodes to prune
	else:
		traverse_tree(root, node.left, nodesToPrune, currentAccuracy, validationDataset)
		traverse_tree(root, node.right, nodesToPrune, currentAccuracy, validationDataset)

# Check if the node can be pruned and prune it if possible
def prune_node(root, node, nodesToPrune, currentAccuracy, validationDataset):
	# Store data of the original node
	originalNode = Node(None, None, None, None)
	originalNode.copy_from(node)

	# Try turning the node into its left leaf
	node.copy_from(node.left)
	accuracyLeft, confusionMatrixLeft, labelDictLeft = evaluate(validationDataset, root)
	node.copy_from(originalNode)

	# Try turning the node into its right leaf
	node.copy_from(node.right)
	accuracyRight, confusionMatrixRight, labelDictRight = evaluate(validationDataset, root)
	node.copy_from(originalNode)

	# Finally, determine if the node can be pruned
	if accuracyLeft >= currentAccuracy[0] or accuracyRight >= currentAccuracy[0]:
		nodesToPrune[0] = True
		originalDepth = node.depth		# We use this to ensure the pruned node still retains its original depth

		if accuracyLeft >= accuracyRight:
			node.copy_from(node.left)
			node.depth = originalDepth
			currentAccuracy[0] = accuracyLeft
		else:
			node.copy_from(node.right)
			node.depth = originalDepth
			currentAccuracy[0] = accuracyRight

	return


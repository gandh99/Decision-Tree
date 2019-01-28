##########################################################################
#                                                                        #
# File Description: Prunes a decision tree that has already been trained #
#                                                                        #
##########################################################################

# Main function to prune the decision tree and then return the pruned tree
def prune_tree(root, originalAccuracy, validationDataset):
	while True:
		nodesToPrune = []
		traverse_tree(root, nodesToPrune)		# Get the list of nodes to prune by traversing the entire tree
		if not nodesToPrune:					# Return if list of nodesToPrune is empty
			return root
		else:
			prune_nodes(nodesToPrune, originalAccuracy, validationDataset)

# Traverse the tree looking for nodes connected to 2 leaves and then add them to the list of nodesToPrune
def traverse_tree(node, nodesToPrune):
	# Return if the node is a leaf
	if node.terminalValue != None:
		return
	# If the node is connected to 2 leaves, attempt to prune it
	elif node.left.terminalValue != None and node.right.terminalValue != None:
		nodesToPrune.append(node)
		return
	# Otherwise continue traversing the tree to look for nodes to prune
	else:
		traverse_tree(node.left, nodesToPrune)
		traverse_tree(node.right, nodesToPrune)

# TODO: Check if the node can be pruned and prune it if possible
# NOTE TO SELF: Will this lead to dangling nodes? Need to re-think feasibility
def prune_nodes(nodesToPrune, originalAccuracy, validationDataset):
	return


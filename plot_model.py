# Testing matplotlib
# https://matplotlib.org/gallery/text_labels_and_annotations/fancytextbox_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancytextbox-demo-py
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.text.html

import matplotlib.pyplot as plt
nodeDict = {}
nodePrint = {}
offsetDict = {	
			0: 0.40,
			1: 0.35,
			2: 0.30,
			3: 0.25,
			4: 0.20,
			5: 0.15,
			6: 0.10,
			7: 0.05,
			8: 0.05,
			9: 0.05,
			10: 0.05, 
			11: 0.05,
			12: 0.05,
			13: 0.05
			}

def plot_tree(node):
	# Version 1
	# startX = 0.5
	# startY = 1.1
	# plot_node(node, startX, startY, None, True)
	# plt.show()

	# Version 2
	global nodeDict
	global nodePrint
	calculate_node_dict(node,)
	calculate_node_print()
	generate_node(node)
	plt.show()

# Testing
def calculate_node_dict(node):
	global nodeDict

	if node.depth in nodeDict:
		nodeDict[node.depth] += 1
	else:
		nodeDict[node.depth] = 1

	if node.terminalValue != None:
		return
	calculate_node_dict(node.left)
	calculate_node_dict(node.right)

# Testing
def calculate_node_print():
	global nodeDict
	global nodePrint

	x = -0.1
	y = 1.0
	nodePrint = dict.fromkeys(nodeDict)
	for key in nodePrint:
		nodePrint[key] = {"x": x, "y": y}
		y -= 0.07

# Testing
def generate_node(node):
	global nodePrint

	draw_node(nodePrint[node.depth]["x"], nodePrint[node.depth]["y"], get_text(node))
	
	# Update nodePrint
	x = 0.07
	nodePrint[node.depth]["x"] += x
	if node.terminalValue != None:
		return
	generate_node(node.left)
	generate_node(node.right)		

# Testing
def get_text(node):
	if node.terminalValue == None:
		return "X" + str(node.splitAttribute) + " < " + str(node.splitValue)
	else:
		return "Label: " + str(node.terminalValue)

# Version 1
def plot_node(node, x, y, branch, root):
	# Extract the correct text to print
	if node.terminalValue == None:
		word = "X" + str(node.splitAttribute) + " < " + str(node.splitValue)
	else:
		word = "Label:" + str(node.terminalValue)

	# Draw the node
	draw_node(x, y, word)

	# Determine the correct offset
	global offsetDict
	verticalOffset = 0.08
	horizontalOffset = offsetDict[node.depth]

	# Continue plotting until leaf node
	if node.terminalValue != None:
		return
	if root == True:
		root = False
		plot_node(node.left, x - horizontalOffset, y - verticalOffset, "left", root) 
		plot_node(node.right, x + horizontalOffset, y - verticalOffset, "right", root)
	else:
		plot_node(node.left, x - horizontalOffset, y - verticalOffset, branch, root) 
		plot_node(node.right, x + horizontalOffset, y - verticalOffset, branch, root)

# Draw the node
def draw_node(x, y, word):
	plt.text(x, y, word, size=30,
		ha="center", va="center",
		bbox=dict(boxstyle="round",
				ec=(.5, 0.5, 0.5),
				fc=(1., 0.8, 0.8),
				), 
		fontsize="x-small"
	)	


if __name__ == "__main__":
	startX = 0.5
	startY = 1.1
	horizontalOffset = 0.05
	verticalOffset = 0.08
	plot_node(node, startX, startY)
	plt.show()


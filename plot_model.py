# Testing matplotlib
# https://matplotlib.org/gallery/text_labels_and_annotations/fancytextbox_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancytextbox-demo-py
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.text.html
# https://stackoverflow.com/questions/36470343/how-to-draw-a-line-with-matplotlib

import matplotlib.pyplot as plt
nodeDict = {}
nodePrint = {}
offsetDict = {	
			0: 0.20,
			1: 0.17,
			2: 0.14,
			3: 0.11,
			4: 0.08,
			5: 0.06,
			6: 0.04,
			7: 0.03,
			8: 0.03,
			9: 0.03,
			10: 0.03, 
			11: 0.03,
			12: 0.03,
			13: 0.03
			}

def plot_tree(node):
	# Version 1
	startX = 0.5
	startY = 1.1
	plot_node(node, startX, startY, None, True)	

	ax = plt.subplot(111)
	pos1 = ax.get_position() # get the original position 
	pos2 = [pos1.x0 - 0.1, pos1.y0 - 0.05,  pos1.width * 1.2, pos1.height * 1.2] 
	ax.set_position(pos2) # set a new position

	axes = plt.gca()	# Set axis
	axes.set_xlim([-0.15,1.05])
	axes.set_ylim([0.0,1.2])
	plt.show()

	# Version 2
	# global nodeDict
	# global nodePrint
	# calculate_node_dict(node,)
	# calculate_node_print()
	# generate_node(node)
	# plt.show()

# Version 2
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

# Version 2
def calculate_node_print():
	global nodeDict
	global nodePrint

	x = -0.1
	y = 1.0
	nodePrint = dict.fromkeys(nodeDict)
	for key in nodePrint:
		nodePrint[key] = {"x": x, "y": y}
		y -= 0.07

# Version 2
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

# Version 1
def plot_node(node, x, y, branch, root):
	# Extract the correct text to print
	if node.terminalValue == None:
		word = get_text(node)
	else:
		word = get_text(node)

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
		draw_line(x, y, x - horizontalOffset, y - verticalOffset)
		draw_line(x, y, x + horizontalOffset, y - verticalOffset)

		plot_node(node.left, x - horizontalOffset, y - verticalOffset, "left", root) 
		plot_node(node.right, x + horizontalOffset, y - verticalOffset, "right", root)
	else:
		draw_line(x, y, x - horizontalOffset, y - verticalOffset)
		draw_line(x, y, x + horizontalOffset, y - verticalOffset)

		plot_node(node.left, x - horizontalOffset, y - verticalOffset, branch, root) 
		plot_node(node.right, x + horizontalOffset, y - verticalOffset, branch, root)

# Draw a node
def draw_node(x, y, word):
	plt.text(x, y, word, size=30,
		ha="center", va="center",
		bbox=dict(boxstyle="round",
				ec=(.5, 0.5, 0.5),
				fc=(1., 0.8, 0.8),
				), 
		fontsize="x-small"
	)

# Draw a line between 2 points
def draw_line(x1, y1, x2, y2):
	x, y = [x1, x2], [y1, y2]
	plt.plot(x, y, marker = 'o')	

# Get the appropriate text to be displayed on the node
def get_text(node):
	if node.terminalValue == None:
		return "X" + str(node.splitAttribute) + "<\n" + str(node.splitValue)
	else:
		return str(node.terminalValue)	


if __name__ == "__main__":
	startX = 0.5
	startY = 1.1
	horizontalOffset = 0.05
	verticalOffset = 0.08
	plot_node(node, startX, startY)


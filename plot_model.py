##########################################################################
#                                                                        #
# File Description: Plots a decision tree that has already been trained  #
#                                                                        #
##########################################################################

# Useful resources:
# https://matplotlib.org/gallery/text_labels_and_annotations/fancytextbox_demo.html#sphx-glr-gallery-text-labels-and-annotations-fancytextbox-demo-py
# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.text.html
# https://stackoverflow.com/questions/36470343/how-to-draw-a-line-with-matplotlib

import matplotlib.pyplot as plt
import numpy as np

# Main function to call for plotting the tree
def plot_tree(node):
	# Begin plotting the tree
	startX = 0.5
	startY = 1.1
	plot_node(node, startX, startY, None, True)	

	# Set the screen
	ax = plt.subplot(111)
	pos1 = ax.get_position() # get the original position 
	pos2 = [pos1.x0 - 0.1, pos1.y0 - 0.05,  pos1.width * 1.2, pos1.height * 1.2] 
	ax.set_position(pos2) # set a new position

	# Set the axis
	axes = plt.gca()	# Set axis
	axes.set_xlim([-0.15,1.05])
	axes.set_ylim([0.0,1.2])
	plt.show()

# Draw the node
def plot_node(node, x, y, branch, root):
	# Extract the correct text to print
	if node.terminalValue == None:
		word = get_text(node)
	else:
		word = get_text(node)

	# Draw the node
	draw_node(x, y, word)

	# Determine the correct offset
	verticalOffset = 0.08
	horizontalOffset = 1 / np.power(node.depth + 1, 2) * (0.5 * node.depth + 1) + 0.3

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



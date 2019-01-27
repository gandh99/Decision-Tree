data = ""

def generate_data(node):
	global data
	traverse_tree(node)	
	print(data)

	return

def traverse_tree(node):
	global data
	if node.terminalValue == None:
		data += get_text(node) + " -> " + get_text(node.left) + "\n"
		data += get_text(node) + " -> " + get_text(node.right) + "\n"
		traverse_tree(node.left)
		traverse_tree(node.right)
	else:
		return 

def get_text(node):
	if node.terminalValue == None:
		return "\"X" + str(node.splitAttribute) + " < " + str(node.splitValue) + "\""
	else:
		return "\"Label: " + str(node.terminalValue) + "\""


class Person:
	def __init__(self, name):
		self.name = name


def change(nodesToPrune):
	nodesToPrune[0] = False

nodesToPrune = [True]
print("Before:", nodesToPrune[0])
change(nodesToPrune)
print("After:", nodesToPrune[0])
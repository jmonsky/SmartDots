from NeuralNetwork import NeuralNetwork
from random import choice

species = []
maxSpecies = 10
inputs = 13
outputs = 2
layers = range(1, 6)
layerSizes = range(2, 15)

def generateSpecies(num):
	global species
	species = []
	for i in range(maxSpecies):
		temp = [choice(layerSizes) for z in range(choice(layers))]
		temp.insert(0, inputs)
		temp.append(outputs)
		species.append(temp)

class Brain(object):
	def __init__(self):
		self.species = choice(species)
		self.speciesString = "Sh:"+str(len(self.species))+":"
		for i in self.species[1:-1]:
			self.speciesString += str(i)
		self.network = NeuralNetwork(self.species)
		self.inputs = [0 for i in range(inputs)]
		self.outputs = [0 for i in range(outputs)]

	def __add__(self, otherBrain):
		pass

	def mutate(self, mr):
		self.network.mutate(mr)

	def copy(self):
		baby = Brain()
		baby.species = self.species
		baby.speciesString = self.speciesString
		baby.network = self.network.copy()
		return baby

	def setInputs(self, arr):
		if len(arr) != len(self.inputs):
			raise Exception("Input array needs to match avaliable inputs: %d != %d" % (len(self.inputs), len(arr)))
		for x,i in enumerate(arr):
			self.inputs[x] = i

	def run(self):
		output = self.network.predict(self.inputs)
		for x,i in enumerate(output):
			self.outputs[x] = i

	def getOutputs(self):
		return self.outputs


if __name__ == "__main__":
	generateSpecies(10)
	test = Brain()
	print(test.speciesString)
	print(test.species)
	test.setInputs([1,2,3,4,5,6,7,8,9,10,11,12,13])
	test.run()
	print(test.getOutputs())
	test2 = test.copy()
	print(test.network.weights[0])
	print(test2.network.weights[0])
	print(test2.network.copy().weights[0])
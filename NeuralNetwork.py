from random import random
import numpy as np
from itertools import product
from math import sin

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def d_sigmoid(y):
	return y * (1 - y)

class NeuralNetwork(object):
	def __init__(self, layer_sizes, alpha = 0.7, seed=None):
		state = np.random.RandomState(seed)
		self.alpha = alpha
		self.weights = [state.uniform(-0.5, 0.5, size)
						for size in zip(layer_sizes[:-1], layer_sizes[1:])]
		self.layer_sizes = layer_sizes

	def copy(self):
		copy = NeuralNetwork(self.layer_sizes)
		copy.weights = []
		for i in self.weights:
			copy.weights.append(i+0)
		return copy
	def mutate(self, mutationRate):
		if abs(mutationRate-1) < 0.000001:
			for x in range(len(self.weights)):
				self.weights[x] = np.random.rand(self.weights[x].shape[0], self.weights[x].shape[1])
		elif mutationRate > 0.0:
			for x in range(len(self.weights)):
				for row in range(len(self.weights[x])):
					for column in range(len(self.weights[x][row])):
						if random() < mutationRate:
							self.weights[x][row][column] = random()
	def __add__(self, other):
		if self.layer_sizes == other.layer_sizes:
			baby = NeuralNetwork(self.layer_sizes)
			for x in range(len(self.weights)):
				for row in range(len(self.weights[x])):
					for column in range(len(self.weights[x][row])):
						if random() > 0.5:
							baby.weights[x][row][column] = self.weights[x][row][column]+0.0
						else:
							baby.weights[x][row][column] = other.weights[x][row][column]+0.0
			return baby

	def _deltas(self, layers, output):
		delta = d_sigmoid(layers[-1]) * (output - layers[-1])
		for layer, w in zip(layers[-2::-1], self.weights[::-1]):
			yield delta
			delta = d_sigmoid(layer) * np.dot(delta, w.T)

	def _learn(self, layers, output):
		deltas = reversed(list(self._deltas(layers, output)))
		return [w + self.alpha * np.outer(layer, delta)
				for w, layer, delta in zip(self.weights, layers, deltas)]

	def train(self, training_data, rounds=5000):
		for _, (input, output) in product(range(rounds), training_data):
			layers = self._feed_forward(np.array(input))
			self.weights = self._learn(list(layers), np.array(output))

	def _feed_forward(self, x):
		yield x
		for w in self.weights:
			x = sigmoid(np.dot(x, w))
			yield x

	def predict(self, input):
		i = np.array(input)
		for layer in self._feed_forward(i): pass
		return layer

if __name__ == "__main__":
	nn = NeuralNetwork([2, 10, 2])
	print(nn.predict([12, 0]))
	print(nn.predict([1, 0]))
from random import randrange, random
from vector import *
from math import cos, sin, radians

class Brain(object):
    def __init__(self, s):
        self.directions = []
        for i in range(s):
            randomAngle = randrange(360)
            self.directions.append(PVector(cos(radians(randomAngle)), sin(radians(randomAngle))))
        self.step = 0
    def mutate(self, mutationRate):
    	for i in range(len(self.directions)):
    		if random() < mutationRate:
    			randomAngle = randrange(360)
    			self.directions[i] = PVector(cos(radians(randomAngle)), sin(radians(randomAngle)))
    def addSteps(self, num):
    	for i in range(num):
    		randomAngle = randrange(360)
    		self.directions.append(PVector(cos(radians(randomAngle)), sin(radians(randomAngle))))
    def clone(self):
    	clone = Brain(len(self.directions))
    	for i in range(len(self.directions)):
    		clone.directions[i] = self.directions[i].copy()
    	return clone
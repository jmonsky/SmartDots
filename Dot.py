from Species import Brain
from vector import PVector, dist
from pygame.draw import circle
from math import radians, degrees
from random import randint

class Dot(object):
	def __init__(self, spawn):
		self.brain = Brain()
		self.species = self.brain.species
		self.speciesString = self.brain.speciesString
		self.pos = spawn
		self.vel = PVector(0,0)
		self.acc = PVector(0,0)
		self.angle = randint(1,360)
		self.dead = False
		self.steps = 0
		self.sight = PVector(10, 0)
		self.reachedGoal = False
		self.fitness = 0.0
		self.spawn = spawn

	def show(self, surface):
		circle(surface, (0,0,0), (int(self.pos.x), int(self.pos.y)), 4)
		circle(surface, (255,0,0), (int(self.pos.x+self.sight.rotate(radians(self.angle)).x), int(self.pos.y+self.sight.rotate(radians(self.angle)).y)), 2)
		##circle(surface, (0,255,0), (int(self.pos.x+self.acc.rotate(radians(self.angle)).x), int(self.pos.y+self.acc.rotate(radians(self.angle)).y)), 2)
		##circle(surface, (0,0,255), (int(self.pos.x+self.vel.rotate(radians(self.angle)).x), int(self.pos.y+self.vel.rotate(radians(self.angle)).y)), 2)

	def update(self, sensoryData):
		## Take in sensory data and create the vector for it
		brainInputs = []
		for z in sensoryData["LeftVision"]: brainInputs.append(z)
		for z in sensoryData["FrontVision"]: brainInputs.append(z)
		for z in sensoryData["RightVision"]: brainInputs.append(z)
		brainInputs.append(sensoryData["Velocity"])
		brainInputs.append(sensoryData["Rotation"])
		brainInputs.append(sensoryData["DegreesToGoal"])
		brainInputs.append(sensoryData["Time"])
		## Take the sensory data and run it through the brain
		self.brain.setInputs(brainInputs)
		self.brain.run()
		brainOutputs = self.brain.getOutputs()


		## Move the dot based on the output
		self.angle += degrees((brainOutputs[0]-0.5)*2)
		self.angle = self.angle%360
		self.acc = PVector(brainOutputs[1]-0.2,0)
		self.vel += self.acc
		self.vel.limit(5)
		self.pos += self.vel.rotate(radians(self.angle))
		self.steps += 1

	def setParent(self, parent):
		self.parentSpecies = parent.species
		self.parentSpeciesString = parent.speciesString

	def mutate(self, mr):
		self.brain.mutate(mr)

	def gimmieBaby(self):
		baby = Dot(self.spawn)
		baby.brain = self.brain
		return baby

	def __add__(self, otherDot):
		baby = Dot()
		baby.brain = self.brain + otherDot.brain
		return baby

	def findFitness(self, goal):
		if self.reachedGoal:
			self.fitness = 1000.0*(1/(self.steps**2))
		else:
			self.fitness = 1.0/(dist(goal, self.pos)**2)
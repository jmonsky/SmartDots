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
		self.startingangle = randint(0,360)
		self.angle = self.startingangle
		self.dead = False
		self.steps = 0
		self.sight = PVector(10, 0)
		self.reachedGoal = False
		self.fitness = 0.0
		self.mutateMe = False
		self.spawn = spawn
		self.isBest = False
		self.radius = 4
		self.color = (0,0,0)
		self.pickedColor = (0,0,255)
		self.bestColor = (0,255,0)

	def show(self, surface):
		if not self.isBest:
			circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
		else:
			circle(surface, self.bestColor, (int(self.pos.x), int(self.pos.y)), int(self.radius*1.5))
		circle(surface, (255,0,0), (int(self.pos.x+self.sight.rotate(radians(self.angle)).x), int(self.pos.y+self.sight.rotate(radians(self.angle)).y)), 2)
		##circle(surface, (0,255,0), (int(self.pos.x+self.acc.rotate(radians(self.angle)).x), int(self.pos.y+self.acc.rotate(radians(self.angle)).y)), 2)
		##circle(surface, (0,0,255), (int(self.pos.x+self.vel.rotate(radians(self.angle)).x), int(self.pos.y+self.vel.rotate(radians(self.angle)).y)), 2)

	def showSelection(self, surface):
		w = surface.get_width()
		h = surface.get_height()

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

	def copy(self):
		baby = Dot(self.spawn)
		baby.brain = self.brain.copy()
		baby.species = self.species
		baby.speciesString = self.speciesString
		return baby

	def exactCopy(self):
		baby = self.copy()
		baby.angle = self.startingangle
		baby.startingangle = self.startingangle
		baby.radius = self.radius
		return baby

	def setParent(self, parent):
		self.parentSpecies = parent.species
		self.parentSpeciesString = parent.speciesString

	def mutate(self, mr):
		if self.mutateMe:
			self.brain.mutate(mr)
			self.mutateMe = False

	def gimmieBaby(self):
		baby = self.copy()
		baby.mutateMe = True
		baby.species = self.species
		baby.speciesString = self.speciesString
		baby.setParent(self)
		return baby

	def __add__(self, otherDot):
		baby = Dot()
		baby.brain = self.brain + otherDot.brain
		return baby

	def findFitness(self, goal):
		distToGoal = dist(goal, self.pos)
		distToSpawn = dist(self.spawn, self.pos)
		if self.reachedGoal:
			self.fitness = 1000.0*(1/(self.steps**2))
		else:
			self.fitness = 1.0/(distToGoal**2)
from Species import Brain
from vector import PVector, dist
from pygame.draw import circle, line
import pygame
from math import radians, degrees
from random import randint, random
from colorsys import hsv_to_rgb

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

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
		self.sight = PVector(20, 0)
		self.allGoalsReached = False
		self.goalsReached = 0
		self.fitness = 0.0
		self.mutateMe = False
		self.spawn = spawn
		self.isBest = False
		self.radius = 4
		self.color = (0,0,0)
		self.pickedColor = (0,0,255)
		self.bestColor = (0,255,0)
		self.seeSight = False
		self.closestDist = 10000
		self.lastSensoryData = {}
		self.deathBy = "None"

	def show(self, surface):
		if not self.isBest:
			circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
		else:
			circle(surface, self.bestColor, (int(self.pos.x), int(self.pos.y)), int(self.radius*1.5))
		if self.seeSight:
			circle(surface, (0,0,0), (int(self.pos.x+self.sight.rotate(radians(self.angle)).x), int(self.pos.y+self.sight.rotate(radians(self.angle)).y)), 2)
			circle(surface, (0,0,0), (int(self.pos.x+self.sight.rotate(radians(self.angle+45)).x), int(self.pos.y+self.sight.rotate(radians(self.angle+45)).y)), 2)
			circle(surface, (0,0,0), (int(self.pos.x+self.sight.rotate(radians(self.angle-45)).x), int(self.pos.y+self.sight.rotate(radians(self.angle-45)).y)), 2)
		##circle(surface, (0,255,0), (int(self.pos.x+self.acc.rotate(radians(self.angle)).x), int(self.pos.y+self.acc.rotate(radians(self.angle)).y)), 2)
		##circle(surface, (0,0,255), (int(self.pos.x+self.vel.rotate(radians(self.angle)).x), int(self.pos.y+self.vel.rotate(radians(self.angle)).y)), 2)

	def showGoal(self, goals, surface):
		circle(surface, (255,255,0), goals[self.goalsReached].integer().toTuple(), 4)

	def showSelection(self, surface, globals):
		w = surface.get_width()
		h = surface.get_height()
		blitText(surface, self.speciesString, (5, int(h*0.5)))
		brainSurface = pygame.Surface((int(w*6/8), int(h*1/4)))
		brainSurface.fill((0, 0, 0))
		CPoint = PVector(int(w/2), int(h*1/5))
		## Draw a bigger dot with orientation and sight info
		filCol = self.color
		rad = self.radius*3
		if self.dead:
			filCol = (255,0,0)
			rad = 0.5*rad 
		if self.isBest:
			if self.dead:
				filCol = (255,255,0)
			else:
				filCol = (0,255,0)
		circle(surface, filCol, (int(CPoint.x), int(CPoint.y)), int(rad))
		if len(self.lastSensoryData.keys()) > 3 and not self.dead:
			CFront = (0,0,0)
			CLeft = (0,0,0)
			CRight = (0,0,0)
			DFront = (self.sight.rotate(radians(self.angle))*5).abs()
			DRight = (self.sight.rotate(radians(self.angle-45))*5).abs()
			DLeft = (self.sight.rotate(radians(self.angle+45))*5).abs()
			if self.lastSensoryData["FrontVision"][1]:
				if self.lastSensoryData["FrontVision"][2] == 0:
					CFront = (255, 0, 0)
				else:
					CFront = (0,255,0)
				DFront = DFront * self.lastSensoryData["FrontVision"][0]
			if self.lastSensoryData["LeftVision"][1]:
				if self.lastSensoryData["LeftVision"][2] == 0:
					CLeft = (255,0,0)
				else:
					CLeft = (0,255,0)
				DLeft = DLeft * self.lastSensoryData["LeftVision"][0]
			if self.lastSensoryData["RightVision"][1]:
				if self.lastSensoryData["RightVision"][2] == 0:
					CRight = (255,0,0)
				else:
					CRight = (0,255,0)
				DRight = DRight * self.lastSensoryData["RightVision"][0]
			circle(surface, CFront, (CPoint+DFront).integer().toTuple(), 5)
			circle(surface, CLeft, (CPoint+DLeft).integer().toTuple(), 5)
			circle(surface, CRight, (CPoint+DRight).integer().toTuple(), 5)
			line(surface, (255,255,255), CPoint.toTuple(), (CPoint+(PVector((self.brain.getOutputs()[1]-0.2)*(40), 0)).rotate(radians(self.angle+(self.brain.getOutputs()[0]-0.5)))).integer().toTuple(), 3)
		## Draw color / sizing options
		## Draw Brain Makeup
		self.brain.render(brainSurface)
		surface.blit(brainSurface, (int(w*1/8), int(h*3/5)))


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
		self.lastSensoryData = sensoryData


		## Move the dot based on the output
		self.angle += degrees((brainOutputs[0]-0.5)*5)
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
			if random() > mr:
				self.startingangle += randint(-10, 10)
				self.angle = self.startingangle

	def gimmieBaby(self):
		baby = self.copy()
		baby.mutateMe = True
		baby.species = self.species
		baby.speciesString = self.speciesString
		baby.setParent(self)
		baby.startingangle = self.startingangle
		baby.angle = self.startingangle
		return baby

	def __add__(self, otherDot):
		baby = Dot()
		baby.brain = self.brain + otherDot.brain
		return baby

	def findFitness(self, goals):
		distToNextGoal = dist(goals[self.goalsReached], self.pos)
		distToSpawn = dist(self.spawn, self.pos)
		self.fitness = 0
		self.fitness += 2.0*(1.0/(self.closestDist**2)) + 1.0/(distToNextGoal**2)
		self.fitness += self.goalsReached
		if self.deathBy == "LastGoal" or self.allGoalsReached:
			self.fitness *= 5
		elif self.deathBy == "Wall":
			self.fitness *= 0.001
		elif self.deathBy == "Circle Of Death":
			self.fitness *= 0
		elif self.deathBy == "Time":
			self.fitness *= 0.5
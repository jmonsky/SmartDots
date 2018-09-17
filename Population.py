from Dot import Dot
from vector import *
from math import atan2
from random import random
import pygame.draw

class Population(object):
	def __init__(self, size, spawnPoint, goals):
		self.dots = []
		self.spawnPoint = spawnPoint
		for i in range(size):
			self.dots.append(Dot(spawnPoint))
		self.generation = 0
		self.goals = goals
		self.maxSteps = 200
		self.step = 0
		self.fitnessSum = 0
		self.nextGen = False
		self.mutationRate = 0.001
		self.randoPerc = 0.10
		self.babyPerc = 0.80
		self.deadGenerations = 0
		self.generations = []

	def show(self, infoSurface, dotSurface):
		if self.step/self.maxSteps > 0.25 and self.step/self.maxSteps < 0.30:
			pygame.draw.circle(dotSurface, (255, 120, 120), (int(self.spawnPoint.x), int(self.spawnPoint.y)), int(dist(self.goals[0], self.spawnPoint)*0.15))
		for dot in self.dots:
			dot.show(dotSurface)
		
	def updateGoals(self, newGoals):
		self.goals = newGoals

	def updateEndpoints(self, spawn, goal):
		self.spawnPoint = spawn
		self.goal = goal
		for dot in self.dots:
			dot.spawn = spawn

	def mutateDemBabies(self):
		for dot in self.dots:
			dot.mutate(self.mutationRate)

	def getGenerationData(self):
		return None

	def naturalSelction(self):
		winners = 0
		for i in self.dots:
			if i.goalsReached > 0:
				winners += 1
		if winners == 0:
			self.deadGenerations += 1
			if self.deadGenerations%2 == 0:
				self.maxSteps += 50
			if self.deadGenerations%3 == 0:
				self.mutationRate += 0.00005
			if self.deadGenerations%5 == 0:
				self.randoPerc += 0.001
				self.babyPerc -= 0.005
		else:
			winPerc = (winners+0.0)/len(self.dots)
			self.deadGenerations = 0
			if winPerc > 0.05:
				self.randoPerc -= 0.001
			if winPerc > 0.15:
				self.mutationRate -= 0.00005
			if winPerc > 0.20:
				self.babyPerc += 0.005

		self.getFitness()
		newDots = []
		bestDot = self.getBest().exactCopy()
		if self.getBest().allGoalsReached:
			self.maxSteps = self.getBest().steps

		randos = int(self.randoPerc * len(self.dots))
		babies = int(self.babyPerc * len(self.dots))
		survivors = len(self.dots) - randos - babies - 1
		for x in range(survivors):
			newDots.append(self.getParent().exactCopy())
		for x in range(babies):
			newDots.append(self.getParent().gimmieBaby())
		for x in range(randos):
			newDots.append(Dot(self.spawnPoint))
		newDots.insert(0, bestDot)
		self.dots = newDots.copy()
		self.generation += 1
		self.nextGen = False
		self.step = 0 
		self.dots[0].isBest = True


	def getBest(self):
		best = self.dots[0]
		for dot in self.dots:
			if dot.fitness > best.fitness:
				best = dot
		return best


	def getFitness(self):
		self.fitnessSum = 0.0
		for dot in self.dots:
			dot.findFitness(self.goals)
			self.fitnessSum += dot.fitness 

	def getParent(self):
		runningSum = 0.0
		rand = random()*self.fitnessSum
		for i in self.dots:
			runningSum += i.fitness
			if runningSum > rand:
				return i
		print("FUCK", runningSum)
		return self.getParent()

	def allDotsDead(self):
		for i in self.dots:
			if not i.dead:
				return False
		return True

	def clickDot(self, x , y):
		m = PVector(x,y)
		for x,dot in enumerate(self.dots):
			if dist(dot.pos, m) < dot.radius*2:
				return x
		else:
			return None

	def update(self, walls):
		if self.step < self.maxSteps and not self.allDotsDead():
			for dot in self.dots:
				if not dot.dead:
					if dist(self.goals[dot.goalsReached], dot.pos) < dot.closestDist:
						dot.closestDist = dist(self.goals[dot.goalsReached], dot.pos)
					sensoryData = {}
					sensoryData["LeftVision"] = [0, 0, 0.5]
					sensoryData["FrontVision"] = [0, 0, 0.5]
					sensoryData["RightVision"] = [0, 0, 0.5]
					for wall in walls:
						if intersect(dot.pos, dot.pos+(dot.vel+dot.acc).rotate(radians(dot.angle)), wall[0], wall[1]):
							dot.dead = True
						else:
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle)), wall[0], wall[1]):
								sensoryData["FrontVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 0]
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle+45)), wall[0], wall[1]):
								sensoryData["LeftVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 0]
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle-45)), wall[0], wall[1]):
								sensoryData["RightVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 0]
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle-45)), self.goals[dot.goalsReached]+PVector(5,0), self.goals[dot.goalsReached]-PVector(5,0)):
						sensoryData["RightVision"] = [dist(dot.pos, self.goals[dot.goalsReached])/dot.sight.mag(), 1, 1]
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle)), self.goals[dot.goalsReached]+PVector(5,0), self.goals[dot.goalsReached]-PVector(5,0)):
						sensoryData["FrontVision"] = [dist(dot.pos, self.goals[dot.goalsReached])/dot.sight.mag(), 1, 1]
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle+45)), self.goals[dot.goalsReached]+PVector(5,0), self.goals[dot.goalsReached]-PVector(5,0)):
						sensoryData["LeftVision"] = [dist(dot.pos, self.goals[dot.goalsReached])/dot.sight.mag(), 1, 1]

					sensoryData["Velocity"] = dot.vel.mag()/5.0
					sensoryData["Rotation"] = dot.angle/360.0
					sensoryData["DegreesToGoal"] = (atan2(self.goals[dot.goalsReached].y-dot.pos.y, self.goals[dot.goalsReached].x-dot.pos.x)-dot.angle)/360.0
					sensoryData["Time"] = self.step/self.maxSteps
					dot.update(sensoryData)
					if dot.steps > self.maxSteps:
						dot.dead = True
						dot.deathBy = "Time"
					if dist(self.goals[dot.goalsReached], dot.pos) < 5:
						dot.goalsReached += 1
						if dot.goalsReached >= len(self.goals):
							dot.dead = True
							dot.allGoalsReached = True
							dot.deathBy = "Last Goal"
					if self.step/self.maxSteps > 0.25 and self.step/self.maxSteps < 0.30:
						if dist(dot.pos, self.spawnPoint) < 0.15*dist(self.spawnPoint, self.goals[0]):
							dot.dead = True
							dot.deathBy = "Circle of Death"
			
			self.step += 1
		else:
			self.nextGen = True

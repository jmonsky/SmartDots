from Dot import Dot
from vector import *
from math import atan2
from random import random
import pygame.draw

class Population(object):
	def __init__(self, size, spawnPoint, goal):
		self.dots = []
		self.spawnPoint = spawnPoint
		for i in range(size):
			self.dots.append(Dot(spawnPoint))
		self.generation = 0
		self.goal = goal
		self.maxSteps = 200
		self.step = 0
		self.fitnessSum = 0
		self.nextGen = False
		self.mutationRate = 0.001
		self.randoPerc = 0.05
		self.babyPerc = 0.80
		self.deadGenerations = 0

	def show(self, infoSurface, dotSurface):
		if self.step/self.maxSteps > 0.25 and self.step/self.maxSteps < 0.30:
			pygame.draw.circle(dotSurface, (255, 120, 120), (int(self.spawnPoint.x), int(self.spawnPoint.y)), int(dist(self.goal, self.spawnPoint)*0.15))
		for dot in self.dots:
			dot.show(dotSurface)
		

	def updateEndpoints(self, spawn, goal):
		self.spawnPoint = spawn
		self.goal = goal
		for dot in self.dots:
			dot.spawn = spawn

	def mutateDemBabies(self):
		for dot in self.dots:
			dot.mutate(self.mutationRate)

	def naturalSelction(self):
		winners = 0
		for i in self.dots:
			if i.reachedGoal:
				winners += 1
		if winners == 0:
			self.deadGenerations += 1

			if self.deadGenerations > 2:
				self.maxSteps += 50
			self.randoPerc += 0.001
			self.babyPerc -= 0.01
		else:
			winPerc = (winners+0.0)/len(self.dots)
			self.deadGenerations = 0
			if winPerc > 0.05:
				self.randoPerc -= 0.001
			if winPerc > 0.15:
				self.mutationRate -= 0.00005
			if winPerc > 0.20:
				self.babyPerc += 0.001

		self.getFitness()
		newDots = []
		bestDot = self.getBest().exactCopy()
		if self.getBest().reachedGoal:
			if self.getBest().steps < self.maxSteps:
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
			dot.findFitness(self.goal)
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

	def update(self, walls):
		if self.step < self.maxSteps and not self.allDotsDead():
			for dot in self.dots:
				if not dot.dead:
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
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle-45)), self.goal+PVector(5,0), self.goal-PVector(5,0)):
						sensoryData["RightVision"] = [dist(dot.pos, self.goal)/dot.sight.mag(), 1, 1]
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle)), self.goal+PVector(5,0), self.goal-PVector(5,0)):
						sensoryData["FrontVision"] = [dist(dot.pos, self.goal)/dot.sight.mag(), 1, 1]
					if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle+45)), self.goal+PVector(5,0), self.goal-PVector(5,0)):
						sensoryData["LeftVision"] = [dist(dot.pos, self.goal)/dot.sight.mag(), 1, 1]

					sensoryData["Velocity"] = dot.vel.mag()/5.0
					sensoryData["Rotation"] = dot.angle/360.0
					sensoryData["DegreesToGoal"] = atan2(self.goal.y-dot.pos.y, self.goal.x-dot.pos.x)
					sensoryData["Time"] = self.step/self.maxSteps
					dot.update(sensoryData)
					if dot.steps > self.maxSteps:
						dot.dead = True
					if dist(self.goal, dot.pos) < 5:
						dot.dead = True
						dot.reachedGoal = True
					if self.step/self.maxSteps > 0.25 and self.step/self.maxSteps < 0.30:
						if dist(dot.pos, self.spawnPoint) < 0.15*dist(self.spawnPoint, self.goal):
							dot.dead = True
			
			self.step += 1
		else:
			self.nextGen = True

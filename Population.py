from Dot import Dot
from vector import *
from math import atan2

class Population(object):
	def __init__(self, size, spawnPoint, goal):
		self.dots = []
		self.spawnPoint = spawnPoint
		for i in range(size):
			self.dots.append(Dot(spawnPoint))
		self.generation = 0
		self.goal = goal
		self.maxSteps = 1000
		self.step = 0
		self.fitnessSum = 0
		self.nextGen = False
		self.mutationRate = 0.001
		self.randoPerc = 0.5

	def show(self, infoSurface, dotSurface):
		for dot in self.dots:
			dot.show(dotSurface)

	def updateEndpoints(self, spawn, goal):
		self.spawnPoint = spawn
		self.goal = goal
		for dot in self.dots:
			dot.spawn = spawn

	def getFitness(self):
		self.fitnessSum = 0
		for dot in self.dots:
			dot.getFitness()
			self.fitnessSum += dot.fitness 




	def update(self, walls):
		if self.step < self.maxSteps:
			for dot in self.dots:
				if not dot.dead:
					sensoryData = {}
					sensoryData["LeftVision"] = [0, 0, 0]
					sensoryData["FrontVision"] = [0, 0, 0]
					sensoryData["RightVision"] = [0, 0, 0]
					for wall in walls:
						if intersect(dot.pos, dot.pos+(dot.vel+dot.acc).rotate(radians(dot.angle)), wall[0], wall[1]):
							dot.dead = True
						else:
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle)), wall[0], wall[1]):
								sensoryData["FrontVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 1]
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle+45)), wall[0], wall[1]):
								sensoryData["LeftVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 1]
							if intersect(dot.pos, dot.pos+dot.sight.rotate(radians(dot.angle-45)), wall[0], wall[1]):
								sensoryData["RightVision"] = [findDist(dot.pos, wall)/dot.sight.mag(), 1, 1]
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
					if self.step/self.maxSteps > 0.10 and self.step/self.maxSteps < 0.15:
						if dist(dot.pos, self.spawnPoint) < 0.25*dist(self.spawnPoint, self.goal):
							dot.dead = True
			if self.step%60:
				print(self.dots[0].brain.inputs, self.dots[0].brain.outputs, self.dots[0].dead, [self.dots[0].pos.x, self.dots[0].pos.y, self.dots[0].angle])

			self.step += 1
		else:
			self.nextGen = True

from Dot import Dot
from time import time
from random import random
class Population(object):
    def __init__(self, s, goal, screen, steps, spawn):
        self.dots = []
        self.fitnessSum = 0.0
        self.generation = 1
        self.minStep = steps
        self.bestDot = 0
        self.mutationRate = 0.01
        self.screen = screen
        self.goal = goal
        self.winPerc = 0
        self.deadGenerations = 0
        self.randoPerc = 0.05
        self.spawn = spawn
        for i in range(s):
            self.dots.append(Dot(goal, screen, steps, spawn))
    
    def show(self, surface, onlybest):
        for i in self.dots:
            if onlybest and self.generation != 1:
                if i.isBest:
                    i.show(surface)
            else:
                i.show(surface)
            
    def update(self, obstacles):
        for i in self.dots:
            if i.brain.step > self.minStep:
                i.dead = True
            else:
                i.update(obstacles)
            
    def caclulateFitness(self):
        for i in self.dots:
            i.calculateFitness()

    def allDotsDead(self):
        for i in self.dots:
            if not i.dead:
                return False
        return True
    
    def getAverageGenome(self):
        averageGenome = []
        for i in self.dots:
            gen = i.getGenome()
            if averageGenome == []:
                averageGenome = gen
            else:
                for x in range(len(gen)):
                    try:
                        averageGenome[x] += gen[x]
                    except:
                        pass
        for i in averageGenome:
            i.x = i.x / len(self.dots)
            i.y = i.y / len(self.dots)
        return averageGenome

    def getBestGenome(self):
        return self.dots[self.bestDot].getGenome()

    def NaturalSelection(self):
        winners = 0
        for i in self.dots:
            if i.reachedGoal:
                self.deadGenerations = 0
                winners += 1
        
        if winners == 0:
            self.deadGenerations += 1
            if self.mutationRate == 0.0:
                self.mutationRate += 0.005
            if self.randoPerc == 0.0:
                self.randoPerc += 0.01
            if self.deadGenerations > 2:
                self.minStep += 50
            if self.deadGenerations > 5:
                self.mutationRate += 0.005
            if self.deadGenerations > 3:
                self.randoPerc += 0.01
        else:
            self.winPerc = winners/len(self.dots)*100
            if self.winPerc > 10:
                self.mutationRate -= 0.001
                if self.mutationRate < 0:
                    self.mutationRate = 0.0001
            if self.winPerc > 80:
                self.randoPerc -= 0.01
                if self.randoPerc < 0:
                    self.randoPerc = 0.0
        if self.randoPerc > 0.30:
            self.randoPerc = 0.30


        self.caclulateFitness()
        newDots = []
        self.calculateFitnessSum()
        self.setBestDot()
        newDots.append(self.dots[self.bestDot].gimmieBaby(self.minStep, self.spawn))
        mutations = int((len(self.dots)-1)*(1-self.randoPerc))
        randos = len(self.dots)-1 - mutations
        for i in range(mutations):
            parent = self.selectParent()
            newDots.append(parent.gimmieBaby(self.minStep, self.spawn))
        for i in range(randos):
            newDots.append(Dot(self.goal, (self.screen), self.minStep, self.spawn))
        self.dots = newDots.copy()
        self.generation += 1
        self.dots[0].isBest = True

    def calculateFitnessSum(self):
        self.fitnessSum = 0.0
        for i in self.dots:
            self.fitnessSum += i.fitness

    def selectParent(self):
        rand = random()*self.fitnessSum
        runningSum = 0
        for i in self.dots:
            runningSum += i.fitness
            if runningSum > rand:
                return i
        return None


    def Mutate(self):
        if self.mutationRate > 0.0:
            for i in self.dots:
                if not i.isBest:
                    i.brain.mutate(self.mutationRate)

    def setBestDot(self):
        best = 0
        self.winPerc = 0
        winners = 0
        for i in range(len(self.dots)):
            if self.dots[i].fitness > best:
                self.bestDot = i
                best = self.dots[i].fitness
        if self.dots[self.bestDot].reachedGoal:
            self.minStep = self.dots[self.bestDot].brain.step
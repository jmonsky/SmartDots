from Brain import Brain
from pygame.draw import circle
from vector import *

def dist(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5

class Dot(object):
    def __init__(self, goal, screen, steps, pos=PVector(10, 10)):
        self.screen = screen
        width = screen[0]
        height = screen[1]
        self.pos = pos.copy()
        self.startpos = pos.copy()
        self.vel = PVector(0,0)
        self.acc = PVector(0,0)
        self.brain = Brain(steps)
        self.radius = 2
        self.color = (0,0,0)
        self.dead = False
        self.goal = goal
        self.fitness = 0.0
        self.reachedGoal = False
        self.isBest = False
    
    def getGenome(self):
        genome = []
        for i in self.brain.directions:
            genome.append(PVector(i.x, i.y))
        return genome

    def show(self, surface):
        if self.isBest:
            circle(surface, (0,255,0), (int(self.pos.x), int(self.pos.y)), self.radius*4)
        else:
            circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        
    def move(self):
        if self.brain.step < len(self.brain.directions):
            self.acc = self.brain.directions[self.brain.step]
            self.brain.step += 1
        else:
            self.dead = True
        
        self.vel += self.acc
        self.pos += self.vel
        self.vel.limit(5)
        
    def update(self, obstacles):
        width = self.screen[0]
        height = self.screen[1]
        if not self.dead and not self.reachedGoal:
            self.move()
            for i in obstacles:
                if i.isIn(self.pos):
                    self.dead = True
            if self.pos.x < self.radius or self.pos.y < self.radius or self.pos.x > width-self.radius or self.pos.y > height-self.radius:
                self.dead = True
            elif dist(self.pos.x, self.pos.y, self.goal.x, self.goal.y) < 5:
                self.reachedGoal = True
                self.dead = True
                
    def calculateFitness(self):
        distanceToGoal = dist(self.pos.x, self.pos.y, self.goal.x, self.goal.y)
        if self.reachedGoal:
            self.fitness = 1.0/16.0 + 10000.0/(self.brain.step**2) 
        else:
            self.fitness = 1.0/(distanceToGoal**2)

    def gimmieBaby(self, newSteps, newPos):
        baby = Dot(self.goal, self.screen, newSteps, newPos)
        baby.brain = self.brain.clone()
        if newSteps > len(self.brain.directions):
            baby.brain.addSteps(newSteps-len(self.brain.directions))
        if len(baby.brain.directions) > newSteps:
            for i in range(len(baby.brain.directions)-newSteps):
                baby.brain.directions.pop()
        return baby
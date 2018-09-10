import pygame, sys
from pygame.locals import *
from Population import Population
from time import time
from mouse import *
from vector import *
from Obstacle import Obstacle
from random import randrange
from colorsys import hsv_to_rgb

def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def setup(width, height):
	global pop, goal
	goal = PVector(width/2, 20)
	pop = Population(1000, goal, SCREENSIZE, 400, SPAWN)
	pygame.display.set_caption("Learning Dots @ Gen: %d" % pop.generation)


def renderGenome(genome, l, h):
	surface = pygame.Surface((l, h))
	size = l/len(genome)
	for x in range(len(genome)):
		i = genome[x]
		UPHUE = abs(i.x+i.y)
		UPCOLOR = hsv_to_rgb(UPHUE, 1, 255)
		rectangle1 = Rect(size*x, 0, size, h)
		pygame.draw.rect(surface, UPCOLOR, rectangle1)
	return surface

def draw(surface):
	global currentStep, GENEAVG, GENEBET, HINDICIE
	surface.fill((255,255,255))
	for i in obstacles:
		i.show(surface)
	if drawRect:
		pygame.draw.rect(surface, (0,0,255), rectangleBuffer, 1)
	pygame.draw.circle(surface, (0,120,120), (int(SPAWN.x), int(SPAWN.y)), 5)
	pygame.draw.circle(surface, (255,0,0), (int(goal.x), int(goal.y)), 5)
	if not PAUSE:
		if pop.allDotsDead():
			pygame.display.set_caption("Learning Dots @ Gen: %d" % pop.generation)
			setIcon(0,0,255)
			avgG = pop.getAverageGenome()
			pop.NaturalSelection()
			pop.Mutate()
			GENEAVG = renderGenome(avgG,genomeSize, 30)
			GENEBET = renderGenome(pop.getBestGenome(),genomeSize, 30)
			BESTHISTORY.append(GENEBET)
			AVERAGEHISTORY.append(GENEAVG)
			currentStep = 0
			HINDICIE -= 1
			if (len(BESTHISTORY)+HINDICIE+1)*65 < height:
				HINDICIE += 1
			setIcon(0,255,0)
		else:
			currentStep += 1
			pop.update(obstacles)
	pop.show(surface, ONLYBEST)
	return surface

def mousePressed(x, y, button):
	global rectangleBuffer, drawRect
	drawRect = True
	rectangleBuffer = Rect(x,y,0,0)
def mouseMoved(x, y, dx, dy, btns):
	global rectangleBuffer, SHOWHELP
	rectangleBuffer.width += dx
	rectangleBuffer.height += dy
	if x < 15 and y > height-30:
		SHOWHELP = True 
	else:
		SHOWHELP = False
def mouseReleased(x, y, button):
	global drawRect
	drawRect = False
def mouseDragged(drag, button):
	flipX, flipY = False, False
	if drag[0][0] > drag[1][0]:
		flipX = True
	if drag[0][1] > drag[1][1]:
		flipY = True
	if flipX:
		firstX = drag[1][0]+0
		secondX = drag[0][0]+0
		drag = ((firstX, drag[0][1]), (secondX, drag[1][1]))
	if flipY:
		firstY = drag[1][1]+0
		secondY = drag[0][1]+0
		drag = ((drag[0][0], firstY), (drag[1][0], secondY))
	obstacles.append(Obstacle(PVector(drag[0][0], drag[0][1]), PVector(drag[1][0]-drag[0][0], drag[1][1]-drag[0][1])))
def mouseClicked(x, y, button):
	if PAUSE:
		if button == 1:
			global goal
			goal.x = int(x)
			goal.y = int(y)
		elif button == 2:
			for p,i in enumerate(obstacles):
				if i.isIn(PVector(x,y)):
					obstacles.pop(p)
					return None
		elif button == 3:
			global SPAWN
			SPAWN.x = int(x)
			SPAWN.y = int(y)


if __name__ == "__main__":
	pygame.init()
	currentStep = 0
	obstacles = []
	GENEAVG = pygame.Surface((0,0))
	GENEBET = pygame.Surface((0,0))
	drawRect = False
	size = width, height = 800, 800
	SCREENSIZE = PVector(width, height)
	STEPS = 400
	rectangleBuffer = Rect(0,0,0,0)
	ONLYBEST = False
	PAUSE = True
	BESTHISTORY = []
	AVERAGEHISTORY = []
	SHOWHISTORY = False
	pygame.display.set_mode(size, RESIZABLE)
	mouse = Mouse()
	SPAWN = PVector(width/2, height-20)
	mouse.setFunctions(mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased)
	pygame.display.set_caption("Learning Dots: PAUSED")
	setIcon(255,255,0)
	setup(width, height)
	HINDICIE = 0
	setIcon(255,0,0)
	genomeSize = int(width*(150/800))
	SHOWHELP = False
	helpTexts = [
		"Welcome To Learning Dots",
		"Press space to pause / unpause",
		"Press 's' to create a new population",
		"Press 'h' to view the genome history",
		"Use arrow keys to navigate history",
		"Use '+' & '-' to change the mutation rate",
		"Use ',' & '.' to change population size",
		"Use '[' * ']' to change maximum step",
		"Use 'o' & 'p' to set match the population step to the (artificial step)",
		"While PAUSED left click to set a goal",
		"While PAUSED right click to set the spawn",
		"While PAUSED click+drag to create obstacles",
		"While PAUSED middle click to remove an obstacle",
		"Press 'u' to remove last placed obstacle",
		"Press 'c' to clear all obstacles",
		"Press 'q' to quit",
	]
	while 1:
		surface = draw(pygame.Surface(size))
		pygame.display.get_surface().blit(surface, (0,0))
		pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 30).render("Generation: %d @ %d%%" % (pop.generation, int(100.0*currentStep/pop.minStep)), True, (0,0,0)), (0,0))
		pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("Mutation Rate: %f" % pop.mutationRate, True, (0,0,0)), (0,30))
		pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("Maximum Step: %d (%d)" % (pop.minStep, STEPS), True, (0,0,0)), (0,45))
		pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("Dots: %d" % len(pop.dots), True, (0,0,0)), (0,60))
		if not SHOWHELP:
			pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 30).render("?", True, (0,0,0)), (0,height-30))
		else:
			for x,i in enumerate(helpTexts):
				pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 30).render(i, True, (255,0,255)), (0,height+30*x-30*len(helpTexts)))


		genomeSize = int(width*(150/800))
		if not SHOWHISTORY:
			pygame.display.get_surface().blit(GENEAVG, (width-genomeSize,0))
			pygame.display.get_surface().blit(GENEBET, (width-genomeSize,30))
			pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("A", True, (0,0,0)), (width-genomeSize-10,5))
			pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("B", True, (0,0,0)), (width-genomeSize-10,35))
		else:
			for X in range(len(AVERAGEHISTORY)):
				if (X+HINDICIE)*65 < height and (X+HINDICIE)*65 >= 0:
					pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("G%d" % (X+1), True, (0,0,0)), (width-genomeSize-(len("G"+str(X+1))*10),X*65+20+65*HINDICIE))
					pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("A", True, (0,0,0)), (width-genomeSize-10,X*65+5+65*HINDICIE))
					pygame.display.get_surface().blit(pygame.font.SysFont("Arial", 15).render("B", True, (0,0,0)), (width-genomeSize-10,X*65+35+65*HINDICIE))
					pygame.display.get_surface().blit(AVERAGEHISTORY[X], (width-genomeSize,X*65+65*HINDICIE))
					pygame.display.get_surface().blit(BESTHISTORY[X], (width-genomeSize,X*65+30+65*HINDICIE))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == VIDEORESIZE:
				width = event.w
				height = event.h
				SCREENSIZE.x = width
				SCREENSIZE.y = height
				size = (width, height)
				pygame.display.set_mode((width, height), RESIZABLE)
			if event.type == MOUSEMOTION:
				mouse.move(event.pos[0], event.pos[1])
			if event.type == MOUSEBUTTONDOWN:
				mouse.mouseDown(event.pos[0], event.pos[1], event.button)
			if event.type == MOUSEBUTTONUP:
				mouse.mouseUp(event.pos[0], event.pos[1], event.button)
			if event.type == KEYDOWN:
				key = event.unicode
				if event.key == K_UP:
					HINDICIE += 1
					if HINDICIE > 0:
						HINDICIE = 0
				elif event.key == K_DOWN:
					HINDICIE -= 1
					if (len(BESTHISTORY)+HINDICIE+1)*65 < height:
						HINDICIE += 1
				elif key in "=+":
					pop.mutationRate += 0.0001
				elif key in "1!":
					ONLYBEST = not ONLYBEST
				elif key in "-_":
					pop.mutationRate -= 0.0001
				elif key in " ":
					PAUSE = not PAUSE
					if PAUSE:
						pygame.display.set_caption("Learning Dots: PAUSED")
						setIcon(255,0,0)
					else:
						pygame.display.set_caption("Learning Dots @ Gen: %d" % pop.generation)
						setIcon(0,255,0)
				elif key in "[{":
					if pop.minStep == STEPS:
						pop.minStep -= 5
					STEPS -= 5
				elif key in "]}":
					if pop.minStep == STEPS:
						pop.minStep += 5
					STEPS += 5
				elif key in "hH":
					SHOWHISTORY = not SHOWHISTORY
				elif key in "qQ":
					pygame.quit()
					sys.exit()
				elif key in "pP":
					pop.minStep = STEPS
				elif key in "oO":
					STEPS = pop.minStep
				elif key in "sS":
					pygame.display.set_caption("Learning Dots: Generating New Population")
					setIcon(255,255,0)
					pop = Population(len(pop.dots), goal, (width, height), STEPS, SPAWN)
					currentStep = 0
					PAUSE = True
					setIcon(255,0,0)
					pygame.display.set_caption("Learning Dots: PAUSED")
					for i in BESTHISTORY:
						del i
					for i in AVERAGEHISTORY:
						del i
					BESTHISTORY = []
					AVERAGEHISTORY = []
				elif key in "cC":
					obstacles = []
				elif key in "uU":
					obstacles.pop()
				elif key in ".>":
					from Dot import Dot
					for i in range(100):
						pop.dots.append(Dot(goal, (width, height), STEPS, SPAWN))
				elif key in ",<":
					for i in range(100):
						if len(pop.dots) > 5:
							pop.dots.pop(randrange(len(pop.dots)))
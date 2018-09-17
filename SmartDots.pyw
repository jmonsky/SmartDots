import pygame, sys
from pygame.locals import *
from time import time
from mouse import *
from vector import *
from random import randrange, randint, random
from colorsys import hsv_to_rgb
from Species import generateSpecies
from Population import Population

"""
TODOS:


REMOVE GOAL SYSTEM AND GRADE BASED ON DISTANCE OBTAINED
FIND A WAY TO MEASURE A "GOOD" DISTANCE
BASICALLY LAPS AROUND A TRACK

TO DO THIS I NEED TO:
	- Remove goals from the population class / fitness functions
	- Remove goals from the nerual network input and just have pure vision
	- Remove time from neural network input


ADD TRACK DESIGNER / SAVER
EXPORT A NN OF A BRAIN OF A DESIRED DOT


"""


def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

def within(x, y, l, t, w, h):
	if x > l and x < l+w:
		if y > t and y < t+h:
			return True
	return False

def keyPressed(key, unicode):
	if not ISTYPE:
		global PAUSE
		if unicode == " ":
			if PAUSE:
				PAUSE = False
				setIcon(0,255,0)
			else:
				PAUSE = True
				setIcon(0,255,255)
		elif unicode.lower() == "q":
			pygame.quit()
			sys.exit()
		elif unicode.lower() == "r":
			global pop
			pop = Population(len(pop.dots), spawn, goals)
	if ISTYPE:
		global TYPING
		if unicode not in ["", ""]:
			TYPING += unicode
		elif unicode == "" and len(TYPING) > 0:
			TYPING = TYPING[:-1]
def keyHeld(key, unicode, time):
	pass



def mouseClicked(x, y, button):
	global SELECTION
	if within(x,y,200,0,int((width - 200)*3/4),int(height*5/6)):
		if button == 1:
			c = pop.clickDot(x-200,y)
			if c != None:
				SELECTION = (c, True)
			else:
				SELECTION = (0, False)
		elif button == 3:
			SELECTION = (0, False)
		elif button == 2:
			if 304 not in keysDown.keys():
				keysDown[304] = 0
			if keysDown[304] != 0.0:
				goals.insert(0, PVector(x-200, y))
			else:
				goals.append(PVector(x-200, y))
			pop.updateGoals(goals)
	if within(x,y,200+int((width - 200)*3/4),0,width-200-int((width - 200)*3/4),int(height*5/6)):
		x = x-200-int((width - 200)*3/4)
		if dist(PVector(125, int(height*5/6)-10), PVector(x,y)) < 7:
			SELECTION = (randint(0, len(pop.dots)-1), True)
def mouseDragged(drag, button):
	if button == 3:
		st = PVector(drag[0][0]-200, drag[0][1])
		sp = PVector(drag[1][0]-200, drag[1][1])
		if st.x > 0 and st.x < int((width - 200)*3/4) and st.y > 0 and st.y < int(height*5/6):
			if sp.x > 0 and sp.x < int((width - 200)*3/4) and sp.y > 0 and sp.y < int(height*5/6): 
				walls.append((st, sp))
def mouseReleased(x, y, button):
	pass
def mousePressed(x, y, button):
	if button == 6:
		if len(walls) > 0:
			walls.pop()
def mouseMoved(x, y, dy, dx, button):
	pass


def init():
	global walls, walls, pop
	global SELECTION, PAUSE
	global TYPING, ISTYPE
	global goals
	TYPING = ""
	ISTYPE = False
	PAUSE = False
	SELECTION = (0, False)
	generateSpecies(settings["Species Count"])
	global spawn, goal 
	W = int((width - 200)*3/4)
	H = int(height*5/6)
	spawn = PVector(W/2, H-50)
	goals = [PVector(W/2, 50)]
	pop = Population(50, spawn, goals)
	walls = []


def run():
	if not PAUSE:
		## Create Imaginary walls along the border of the map to kill off idiots
		w = walls.copy()
		w.append([PVector(0,0), PVector(int((width - 200)*3/4), 0)])
		w.append([PVector(0,0), PVector(0,int(height*5/6))])
		w.append([PVector(int((width - 200)*3/4),0), PVector(int((width - 200)*3/4),int(height*5/6))])
		w.append([PVector(0,int(height*5/6)), PVector(int((width - 200)*3/4),int(height*5/6))])
		## Run the update on the population

		pop.update(w)
		## Check if its time to move to the next generation
		if pop.nextGen:
			global SELECTION
			SELECTION = (0, False)
			pop.naturalSelction()
			pop.mutateDemBabies()

def draw(surface):
	## Cut up the screen
	drawWidth = int((width - 200)*3/4)
	statWidth = int(width*3/4)
	height1 = int(height*5/6)
	height2 = height - height1
	## Create the surfaces
	StatSurface = pygame.Surface((statWidth, height2))
	ControlSurface = pygame.Surface((width-statWidth, height2))
	DrawSurface = pygame.Surface((drawWidth, height1))
	MapEditSurface = pygame.Surface((200, height1))
	InfoSurface = pygame.Surface((width-drawWidth-200, height1))
	## Fill the surface's backgrounds
	StatSurface.fill((255,0,0))
	ControlSurface.fill((0,255,0))
	DrawSurface.fill((255,255,255))
	MapEditSurface.fill((0,0,255))
	InfoSurface.fill((150,150,150))
	surface.fill((0,0,0))
	## Draw the Dots
	pop.show(InfoSurface, DrawSurface)

	## Draw the obstacles
	for w in walls:
		pygame.draw.line(DrawSurface, (0,0,255), w[0], w[1], 4)
	## Draw the goal and spawn
	for goal in goals:
		pygame.draw.circle(DrawSurface, (255,0,0), (int(goal.x), int(goal.y)), 5)
	pygame.draw.circle(DrawSurface, (0,0,255), (int(spawn.x), int(spawn.y)), 5)
	## Draw the Overlay
	
	if SELECTION[1]:
		pop.dots[SELECTION[0]].showSelection(InfoSurface, (PAUSE, True))
		pop.dots[SELECTION[0]].showGoal(goals, DrawSurface)
	STRINGSTACK = [
		 "Select Random Dot:",
		 "Mutation Rate: %.2f%%" % (pop.mutationRate*100),
		 "Babys: %.2f%%" % (pop.babyPerc*100),
		 "Randoms: %.2f%%" % (pop.randoPerc*100),
		 "Survivors: %.2f%%" % ((1-pop.babyPerc-pop.randoPerc)*100)

	]
	pygame.draw.circle(InfoSurface, (120, 180, 180), (125, height1-10), 7)
	for i in range(len(STRINGSTACK)):
		blitText(InfoSurface, STRINGSTACK[i], (5, height1-15*(i+1)-5))
	## Blit the surfaces to the screen
	surface.blit(StatSurface, (0, height1))
	surface.blit(ControlSurface, (statWidth, height1))
	surface.blit(DrawSurface, (200, 0))
	surface.blit(MapEditSurface, (0, 0))
	surface.blit(InfoSurface, (drawWidth+200, 0))	
	return surface


if __name__ == "__main__":

	## Create the screen
	size = width, height = 1200, 800
	SCREENSIZE = PVector(width, height)
	pygame.init()
	pygame.display.set_mode(size, RESIZABLE)
	pygame.display.set_caption("Smart Dots")
	setIcon(255,0,0)
	## Create the mouse tracker / key trackers
	mouse = Mouse()
	mouse.setFunctions(mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased)
	keysDown = dict()
	unicodes = dict()
	## Ignore these 'bad' keys, was a temporary solution to abug
	#badKeys = [301, 303, 304, 305, 306, 273, 274, 275, 276, 311, 319, 127, 277, 279, 278, 280, 281, 316, 300, 19, 302] + [x for x in range(282, 294)]
	badKeys = []
	## Create the timer variables
	frameRate = 60
	frameTime = 1/frameRate
	lFrame = 0
	runRate = 120
	runTime = 1/runRate
	lRun = 0
	## Create Settings Variable
	settings = {"Species Count":50}

	## Run the init function
	init()
	setIcon(0,255,0)
	while 1:
		## Run the clock stuff
		if abs(time() - lRun) > runTime:
			run()
			lRun = time()

		if abs(time() - lFrame) > frameTime:
		## Draw stuff to the screen
			mainSurface = draw(pygame.Surface(size))
			pygame.display.get_surface().blit(mainSurface, (0,0))
			lFrame = time()
		pygame.display.flip()

		## Handle inputs and events
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
				if width < 800:
					width = 800
					SCREENSIZE.x = width
					pygame.display.set_mode((width, height), RESIZABLE)
				if height < 600:
					height = 600
					SCREENSIZE.y = height
					pygame.display.set_mode((width, height), RESIZABLE)
			if event.type == MOUSEMOTION:
				mouse.move(event.pos[0], event.pos[1])
			if event.type == MOUSEBUTTONDOWN:
				mouse.mouseDown(event.pos[0], event.pos[1], event.button)
			if event.type == MOUSEBUTTONUP:
				mouse.mouseUp(event.pos[0], event.pos[1], event.button)
			if event.type == KEYDOWN:
				if event.key not in badKeys:
					if event.key in keysDown.keys():
						if keysDown[event.key] == 0.0:
							keysDown[event.key] = time()
							keyPressed(event.key, event.unicode)
						else:
							keyHeld(event.key, event.unicode, time()-keysDown[event.key])
					else:
						keysDown[event.key] = time()
						keyPressed(event.key, event.unicode)
			if event.type == KEYUP:
				if event.key not in badKeys:
					if keysDown[event.key] != 0:
						keysDown[event.key] = 0.0
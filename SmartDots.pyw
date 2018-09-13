import pygame, sys
from pygame.locals import *
from time import time
from mouse import *
from vector import *
from random import randrange, randint, random
from colorsys import hsv_to_rgb
from Species import generateSpecies
from Population import Population

def setIcon(R, G, B):
	icon = pygame.Surface((32, 32))
	icon.fill((R,G,B))
	pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
	surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)


def keyPressed(key, unicode):
	pass
def keyHeld(key, unicode, time):
	pass
def keyReleased(key, unicode, time):
	pass

def mouseClicked(x, y, button):
	pass
def mouseDragged(drag, button):
	st = PVector(drag[0][0]-200, drag[0][1])
	sp = PVector(drag[1][0]-200, drag[1][1])
	if st.x > 0 and st.x < int((width - 200)*3/4) and st.y > 0 and st.y < int(height*5/6):
		if sp.x > 0 and sp.x < int((width - 200)*3/4) and sp.y > 0 and sp.y < int(height*5/6): 
			walls.append((st, sp))
def mouseReleased(x, y, button):
	pass
def mousePressed(x, y, button):
	pass
def mouseMoved(x, y, dy, dx, button):
	pass


def init():
	global walls, walls, pop
	generateSpecies(settings["Species Count"])
	global spawn, goal 
	W = int((width - 200)*3/4)
	H = int(height*5/6)
	spawn = PVector(W/2, H-50)
	goal = PVector(W/2, 50)
	pop = Population(200, spawn, goal)
	walls = []


def run():
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
	InfoSurface.fill((255,0,255))
	surface.fill((0,0,0))
	## Draw the Dots
	pop.show(InfoSurface, DrawSurface)

	## Draw the obstacles
	for w in walls:
		pygame.draw.line(DrawSurface, (0,0,255), w[0], w[1], 2)
	## Draw the goal and spawn
	pygame.draw.circle(DrawSurface, (255,0,0), (int(goal.x), int(goal.y)), 5)
	pygame.draw.circle(DrawSurface, (0,0,255), (int(spawn.x), int(spawn.y)), 5)
	## Draw the Overlay
	
	

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
	## Create the timer variables
	frameRate = 60
	frameTime = 1/frameRate
	lFrame = 0
	runRate = 1000
	runTime = 1/runRate
	lRun = 0
	## Create Settings Variable
	settings = {"Species Count":20}

	## Run the init function
	init()
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
				if event.key in keysDown.keys():
					if keysDown[event.key] == 0.0:
						keysDown[event.key] = time()
						keyPressed(event.key, event.unicode)
						unicodes[event.key] = event.unicode.lower()
					else:
						keyHeld(event.key, event.unicode, time()-keysDown[event.key])
				else:
					keysDown[event.key] = time()
					keyPressed(event.key, event.unicode)
					unicodes[event.key] = event.unicode.lower()
			if event.type == KEYUP:
				if keysDown[event.key] != 0:
					keyReleased(event.key, unicodes[event.key], time() - keysDown[event.key])
					keysDown[event.key] = 0.0
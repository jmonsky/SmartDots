from pygame.draw import rect
from pygame import Rect
class Obstacle(object):
	def __init__(self, pos, size):
		self.pos = pos
		self.size = size
	def isIn(self, point):
		if point.x > self.pos.x and point.x < self.pos.x + self.size.x and point.y > self.pos.y and point.y < self.pos.y + self.size.y:
			return True
		else:
			return False
	def show(self, surface):
		rect(surface, (0,0,255), Rect(self.pos.x, self.pos.y, self.size.x, self.size.y))
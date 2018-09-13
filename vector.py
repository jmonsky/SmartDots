from math import atan2, cos, sin, fabs, radians, degrees, sqrt
import numpy as np
from numpy.linalg import norm

class PVector(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		
	def __add__(self, otherV):
		if isinstance(otherV, PVector):
			return PVector(self.x+otherV.x, self.y+otherV.y)

	def __sub__(self, otherV):
		if isinstance(otherV, PVector):
			return PVector(self.x-otherV.x, self.y-otherV.y)
	def mag(self):
		return sqrt((self.x)**2+(self.y)**2)

	def angle(self):
		return atan2(self.y, self.x)

	def limit(self, mag):
		if self.mag() > mag:
			ang = self.angle()
			self.x = cos(ang)*mag
			self.y = sin(ang)*mag

	def byMag(self, mag, dir):
		self.x = cos(dir)*mag
		self.y = sin(dir)*mag
		return self


	def rotate(self, angle):
		return PVector().byMag(self.mag(), self.angle()+angle)

	def copy(self):
		return PVector(self.x, self.y)

	def __str__(self):
		return str((self.x, self.y))

	def __getitem__(self, x):
		if x == 0:
			return self.x
		elif x == 1:
			return self.y
		else:
			return 0

	def __len__(self):
		return 2

	def toNP(self):
		return np.array([self.x, self.y])

def dist(p1, p2):
	return sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2)

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def findDist(point, line):
	p1 = line[0].toNP()
	p2 = line[1].toNP()
	p3 = point.toNP()
	return np.cross(p2-p1,p3-p1)/norm(p2-p1)

if __name__ == "__main__":
	test2 = PVector(10, 10)
	print(degrees(test2.angle()))
	test3 = test2.rotate(radians(90))
	print(degrees(test3.angle()))
	print(test3.x, test3.y)

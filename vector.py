from math import atan2, cos, sin, fabs, radians, degrees

class PVector(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		
	def __add__(self, otherV):
		if isinstance(otherV, PVector):
			return PVector(self.x+otherV.x, self.y+otherV.y)

	def mag(self):
		return ((self.x)**2+(self.y)**2)**0.5

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

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

for D in range(0, 900):
	person = PVector(0,0)
	sight = PVector().byMag(15, radians(D/10))
	randomTangentStart = PVector(0,20)
	randomTangentEnd = PVector(20,0)
	print(D/10, intersect(person, person+sight, randomTangentStart, randomTangentEnd))
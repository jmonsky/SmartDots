from Species import Brain

class Dot(object):
	def __init__(self):
		pass


	def show(self, surface):
		pass
	def update(self):
		pass

	def mutate(self, mr):
		pass
	def gimmieBaby(self):
		pass
	def __add__(self, otherDot):
		baby = Dot()
		baby.brain = self.brain + otherDot.brain
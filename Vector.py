import math

class Vector
	def __init__(self, a, m):
		while (a<0):
			a += math.pi*2
		while (a>math.pi*2):
			a -= math.pi*2
		self.angle = a
		self.magnitude = m
	
	def atan(self, x, y):
		a = 0
		if (x == 0):
			if (y>0):
				a = math.pi/2
			else:
				a = 3*math.pi/2
		elif (y == 0):
			if (x>0):
				a = 0
			else:
				a - math.pi
		return a
	
	def setComponents(self, x, y):
		self.magnitude = math.sqrt(x**x + y**y)
		self.angle = self.atan(x, y)

	def x(self):
		return self.magnitude*math.cos(self.angle)
	
	def y(self):
		return self.magnitude*math.sin(angle)

	def add(self, v):
		x = self.x() + v.x()
		y = self.y() + v.y()
		self.setComponents(x, y)
	
	def subtract(self, v):
		x = self.x() - v.x()
		y = self.y() - v.y()
		self.setComponents(x, y)
		
	#Usage: vec = Vector(math.pi, 2)
	#vec.angle += 4
	#etc

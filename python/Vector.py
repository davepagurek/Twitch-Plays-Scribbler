import math

class Vector:
	def __init__(self, a, m):
		while (a<0):
			a += 360
		while (a>360):
			a -= 360
		self.angle = float(a)
		self.magnitude = float(m)

	def atan(self, x, y):
		a = 0
		if (x == 0):
			if (y>0):
				a = 90
			else:
				a = 270
		elif (y == 0):
			if (x>0):
				a = 0
			else:
				a = 180
		else:
			a = (math.atan(y/x)/(math.pi))*180
			if (a<0):
				a += 180
		return a

	def setComponents(self, x, y):
		self.magnitude = math.sqrt(x**x + y**y)
		self.angle = self.atan(x, y)

	def x(self):
		return self.magnitude*math.cos((self.angle/180)*math.pi)

	def y(self):
		return self.magnitude*math.sin((self.angle/180)*math.pi)

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

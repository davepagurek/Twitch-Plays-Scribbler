from myro import *

init()

threshold = 4000

while 1:

	forward(1, 0.2)

	if (getObstacle("center")>threshold or getObstacle("left")>threshold):
		while (getObstacle("center")>threshold or getObstacle("left")>threshold):
			turnRight(1, 0.5)
			forward(1, 0.5)
			turnLeft(1, 0.5)

	elif (getObstacle("right")>threshold):
		while (getObstacle("right")>threshold):
			turnLeft(1, 0.5)
			forward(1, 0.5)
			turnRight(1, 0.5)

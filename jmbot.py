from myro import *

init()
# 0-7000 value for proximity of obstacle
threshold = 4000

setName("JMBOT");
while 1:
        #starts moving robot forward
	forward(1)
        # if the obstacle is left or in the centre, then turn right
	if (getObstacle("center")>threshold or getObstacle("left")>threshold):
		while (getObstacle("center")>threshold or getObstacle("left")>threshold):
			stop()
			turnRight(1, 0.5)
			forward(1, 0.5)
			turnLeft(1, 0.5)
			stop()
        # if the obstacle is to the right, turn the robot left
	elif (getObstacle("right")>threshold):
		while (getObstacle("right")>threshold):
			stop()
			turnLeft(1, 0.5)
			forward(1, 0.5)
			turnRight(1, 0.5)
			stop()
# method that can be implemented to check if there is an object
def checkIfObject():
    if(getObstacle("right") >threshold or getObstacle("center")>threshold or getObstacle("left")>thresholdr )
        return True;

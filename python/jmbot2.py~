from myro import *

init("/dev/rfcomm1")
# 0-7000 value for proximity of obstacle
objectarray=[0,0,0]
threshold = 100
setIRPower(135)
setName("JMBOT")
setForwardness(1)
forward(1)

#returns an list with the proximity values from  IR sensors
"""Method to return array in the form [left, center,right]"""
def getData():
	left=getObstacle("left")	
    	right=getObstacle("right")
    	center=getObstacle("center")
    	return [left,center,right]
# method that can be implemented to check if there is an object
def checkIfObject():
    #quick check to see if any object
    	if(getObstacle("right") > threshold or getObstacle("center") > threshold or getObstacle("left") > threshold):
        return True

def isObjectLeft(a):
    	if((a[1]>threshold or a[0]>threshold)):
        	return True
    	else:
        	return False
def isObjectRight(a):
    	if((a[2]>threshold)):
        	return True
    	else:
        	return False
        """return 0 for left, 1 for center, 2 for right"""
def move()
	"""Get the data of sensor"""
	direction = getData()
	"""generate counter for displacement of right and left"""
	rightCount = 0
	leftCount = 0
	"""Check where is the object"""
	while (checkIfObject()):
		stop()
		"""If the object is to the left or center, turn right"""
		if (isObjectLeft(direction)):
			stop()
			turnRight(1,0.5)
			forward(1,0.5)
			rightCount++
			""""If the reobot didn't came back to its main position"""
			while(rightCount>0):
				stop()
				turnLeft(1, 0.5)
				"""Check if there is any object to the left"""
				"""If there is, turn back and go straight"""
				if(isObjectLeft(direction)):
					stop()
					turnRight(1,0.5)
					forward(1,0.5)
					rightCount++
				"""If there is none, go forward until Count = 0"""
				else:
					stop()
					forward(1, 0.5)
					rightCount--
			"""When it went back to original position, go back to the original track"""
			stop()
			turnRight(1,0.5)
			forward(1, 0.5)
		"""If the object is to the right, turn left"""
		elif (isObjectRight(direction)):
			stop()
			turnLeft(1,0.5)
			forward(1,0.5)
			leftCount++
			""""If the reobot didn't came back to its main position"""
			while(leftCount>0):
				stop()
				turnRight(1, 0.5)
				"""Check if there is any object to the Right"""
				"""If there is, turn back and go straight"""
				if(isObjectRight(direction)):
					stop()
					turnLeft(1,0.5)
					forward(1,0.5)
					leftCount++
				"""If there is none, go forward until Count = 0"""
				else:
					stop()
					forward(1, 0.5)
					leftCount--
			"""When it went back to original position, go back to the original track"""
			stop()
			turnLeft(1,0.5)
			forward(1, 0.5)
				
			
			


while 1:
    #Debug
    objectarray=getData()
    print str(objectarray[0])+" "+str(objectarray[1])+" "+str(objectarray[2])
    # if the obstacle is left or in the centre, then turn right
   move()

    forward(1)




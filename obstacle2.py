from myro import *

init("/dev/rfcomm0")
# 0-7000 value for proximity of obstacle
objectarray=[0,0,0]
threshold = 100
cycle = 1
setIRPower(130)
setName("JMBOT")
setForwardness(1)
forward(1)
cleared = False

#returns an list with the proximity values from  IR sensors
"""Method to return array in the form [left, center,right]"""
def getData():
    left = 0
    right = 0
    center = 0
    for i in range(3):
        left+=getObstacle("left")
        right+=getObstacle("right")
        center+=getObstacle("center")
    left /= 3
    right /= 3
    center /= 3
    return [left,center,right]
def isObject(a):
    if(a[0]>threshold or a[1]>threshold or a[2]>threshold):
        return True
    else:
        return False
def isObjectLeft(a):
    if((a[0]>threshold) and (a[0]>a[2])):
        return True
    else:
        return False
def isObjectRight(a):
    if((a[2]>threshold) and a[2]>a[0] and a[2]>a[1]):
        return True
    else:
        return False
        """return 0 for left, 1 for center, 2 for right"""
def printData(objectarray):
        print str(objectarray[0])+" "+str(objectarray[1])+" "+str(objectarray[2])

def getDirection(a):
    #object to the left, send turn right command
    if(a[0]>threshold and a[0]>a[2]):
        return 2
    #object to the right, turn left
    elif(a[2]>threshold and a[2]>a[0]):
        return 0
    #center has most clear path
    elif(a[1]<=a[0] and a[1]<=a[2]):
        return 1;

def tryForward(time, direction, num, overshoot=0):
    turnTime = 0.75
    step = 0.5
    fwd = 1
    side = 1
    obstacles = getData()

    #Go around then come back if there's an obstacle
    if (direction == 0 and isObject(obstacles)):
    	speak("Holy shit")
        # print("Cycle: " + str(num) + " (Object to left)")
        turnRight(1, turnTime)
        tryForward(side, 0, num+1)
        turnLeft(1, turnTime)
        tryForward(fwd, 0, num+1, 1)
    elif (direction == 1 and isObject(obstacles)):
        # print("Cycle: " + str(num) + " (Object to right)")
        speak("Holy shit")
        turnLeft(1, turnTime)
        tryForward(side, 1, num+1)
        turnRight(1, turnTime)
        tryForward(fwd, 1, num+1, 1)
    else:
    	if (overshoot):
			if (direction == 0):
				turnRight(1, turnTime)
				tryForward(step, 0, num+1)
				turnLeft(1, turnTime)
			else:
				turnLeft(1, turnTime)
				tryForward(side, 1, num+1)
				turnRight(1, turnTime)
    	t=0
        while (t<time):
            move2(step, num+1)
            t += step
    #else:
        # print("Cycle: " + str(num) + " No objects")
        #forward(1)
        #wait(time)

#Recursively go around objects to end up on the same path
def move2(time, num):
    turnTime = 0.75
    step = 0.5
    fwd = 1
    side = 1
    obstacles = getData()

    #Go around then come back if there's an obstacle
    if (isObjectLeft(obstacles)):
    	speak("Holy shit")
        print("Cycle: " + str(num) + " (Object to left)")
        turnRight(1, turnTime)
        tryForward(side, 0, num+1)
        turnLeft(1, turnTime)
        tryForward(fwd, 0, num+1, 1)
        turnLeft(1, turnTime)
        tryForward(side*1.5, 0, num+1)
        turnRight(1, turnTime)
    elif (isObjectRight(obstacles)):
    	speak("Holy shit")
        print("Cycle: " + str(num) + " (Object to right)")
        turnLeft(1, turnTime)
        tryForward(side, 1, num+1)
        turnRight(1, turnTime)
        tryForward(fwd, 1, num+1, 1)
        turnRight(1, turnTime)
        tryForward(side*1.5, 1, num+1)
        turnLeft(1, turnTime)
    elif (time > step):
        t=0
        while (t<time):
            move2(step, num+1)
            t += step
    else:
        print("Cycle: " + str(num) + " No objects")
        forward(1)
        wait(time)
while 1:
    #Debug
    # if the obstacle is left or in the centre, then turn right
    #move()
    move2(1, cycle)
    #forward(1)




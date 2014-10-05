from myro import *

init("/dev/rfcomm1")
# 0-7000 value for proximity of obstacle
threshold = 100
cycle = 1
cleared = False
steps = 0
rightTurnTime = 0.95
setIRPower(130)
setName("JMBOT")
setForwardness(1)

#returns an list with the proximity values from  IR sensors
"""Method to return array in the form [left, center,right]"""
def getData():
    left = 0
    right = 0
    center = 0
    for x in range(4):
        left+=getObstacle("left")
        right+=getObstacle("right")
        center+=getObstacle("center")
    left /= 4
    right /= 4
    center /= 4
    wait(0.5)
    return [left,center,right]


"""See if there is an object in front of the robot"""
def isObject(a):
    if(a[0]>threshold or a[1]>threshold or a[2]>threshold):
        return True
    else:
        return False

"""See if object takes up more space to the left"""
def isObjectLeft(a):
    if((a[0]>threshold) and (a[0]>a[2])):
        return True
    else:
        return False

"""See if object takes up more space to the right"""
def isObjectRight(a):
    if((a[2]>threshold) and a[2]>a[0]):
        return True
    else:
        return False

"""return 0 for left, 1 for center, 2 for right"""
def getDirection(a):
    #object to the left, send turn right command
    if(isObjectLeft(a)):
        return 0
    #object to the right, turn left
    else:
        return 2
            
def goAround(d):
    print("Going around")
    forward(1, 0.5)
    if (d==2):
        turnLeft(1, rightTurnTime)
    else:
    	turnRight(1, rightTurnTime)
    ##stop()
    obstacles = getData()
    if not (isObject(obstacles)):
    	cleared = True
    	if (d==0):
        	turnLeft(1, rightTurnTime)
        	forward(1, 1)
        	turnRight(1, rightTurnTime)
    	else:
    		turnRight(1, rightTurnTime)
    		forward(1, 1)
        	turnLeft(1, rightTurnTime)
    else:
        if (d==0):
            turnLeft(1, rightTurnTime)
        else:
            turnRight(1, rightTurnTime)

#Recursively go around objects to end up on the same path
def move(num):
    avoidanceMode = False
    ####stop()
    obstacles = getData()
    if isObject(obstacles):
        avoidanceMode = True
    else:
        avoidanceMode = False
        
    #Go around then come back if there's an obstacle(
    if (avoidanceMode):
        path = getDirection(obstacles)
        if (path == 0):
            print("Cycle: " + str(num) + " (Object to left)")
            turnRight(1, rightTurnTime)
            cleared = False
            while not (cleared):
                print("Clearing to the right")
            	goAround(2)
            	++steps
            cleared = False
            while not (cleared):
                print("Clearing to the left")
            	goAround(0)
            while not steps==0:
                print("Returning to main line")
            	goforward(1, 1)
            	--steps
            turnRight(1, rightTurnTime)
        elif (path == 2):
            print("Cycle: " + str(num) + " (Object to right)")
            turnLeft(1, rightTurnTime)
            cleared = False
            while not (cleared):
                print("Clearing to the left")
            	goAround(0)
            	++steps
            cleared = False
            while not (cleared):
                print("Clearing to the right")
            	goAround(2)
            while not steps==0:
                print("Returning to main line")
            	goforward(1, 1)
            	--steps
            turnLeft(1, rightTurnTime)
    else:
        forward(1,1)

while 1:
    #Debug
    # if the obstacle is left or in the centre, then turn right
    #move()
    move(cycle)
    #forward(1)




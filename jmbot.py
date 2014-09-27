from myro import *

init("/dev/rfcomm2")
# 0-7000 value for proximity of obstacle
objectarray=[0,0,0]
threshold = 100
cycle = 1
setIRPower(130)
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
    if((a[1]>threshold or a[0]>threshold) and (a[1]>a[2] or a[0]>a[2])):
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
def move():
    rightcount=0
    a=getData()
    printData(a)
    direction=getDirection(a)
    if direction==0:
        #go right around object
        #continues turning until obstacle is no longer in front
        while (isObjectLeft(a)):
            ++rightcount
            turnRight(1)
            wait(.1)
            a=getData()
            printData(a)
        forward(1)
        # #course correction
        # while(rightcount>0):
        #     turnLeft(1)
        #     wait(.1)
        #     --rightcount
        #      a=getData()
        # forward(1)
    elif direction==1:
        forward(1)
        a=getData()
        printData(a)
    elif direction==2:
        #go left around object
        while isObjectLeft(a):
            ++rightcount
            turnLeft(1)
            a=getData()
            printData(a)
        forward(1)
        #course correction
        # while(rightcount>0):
        #     turnRight(1)
        #     --rightcount
        #     a=getData()
        forward(1)

def tryForward(time, num):
    turnTime = 0.75
    step = 0.5
    fwd = 2
    side = 1
    obstacles = getData()

    #Go around then come back if there's an obstacle
    if (isObjectLeft(obstacles)):
        print("Cycle: " + str(num) + " (Object to left)")
        turnRight(1, turnTime)
        tryForward(side, num+1)
        turnLeft(1, turnTime)
        tryForward(fwd, num+1)
    elif (isObjectRight(obstacles)):
        print("Cycle: " + str(num) + " (Object to right)")
        turnLeft(1, turnTime)
        tryForward(side, num+1)
        turnRight(1, turnTime)
        tryForward(fwd, num+1)
    elif (time > step):
        t=0
        while (t<time):
            tryForward(step, num+1)
            t += step
    else:
        print("Cycle: " + str(num) + " No objects")
        forward(1)
        wait(time)

#Recursively go around objects to end up on the same path
def move2(time, num):
    turnTime = 0.75
    step = 0.5
    fwd = 2
    side = 1
    obstacles = getData()

    #Go around then come back if there's an obstacle
    if (isObjectLeft(obstacles)):
        print("Cycle: " + str(num) + " (Object to left)")
        turnRight(1, turnTime)
        tryForward(side, num+1)
        turnLeft(1, turnTime)
        tryForward(fwd, num+1)
        turnLeft(1, turnTime)
        tryForward(side, num+1)
        turnRight(1, turnTime)
    elif (isObjectRight(obstacles)):
        print("Cycle: " + str(num) + " (Object to right)")
        turnLeft(1, turnTime)
        tryForward(side, num+1)
        turnRight(1, turnTime)
        tryForward(fwd, num+1)
        turnRight(1, turnTime)
        tryForward(side, num+1)
        turnLeft(1, turnTime)
    elif (time > step):
        t=0
        while (t<time):
            tryForward(step, num+1)
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




from myro import *

init("/dev/rfcomm1")
# 0-7000 value for proximity of obstacle
threshold = 100
setIRPower(135)
setName("JMBOT")
forward(1)

def getData():
    left=getObstacle("left")
    right=getObstacle("right")
    center=getObstacle("center")
    return [left,center,right]

while 1:

    #starts moving robot forward

    #Debug
    objectarray=getData()
    print str(objectarray[0])+" "+str(objectarray[1])+" "+str(objectarray[2])
    # if the obstacle is left or in the centre, then turn right
    if (objectarray[1]>threshold or objectarray[0]>threshold):
        while (objectarray[1]>threshold or objectarray[0]>threshold):
            stop()
            turnRight(1, 0.5)
            forward(1, 0.5)
            turnLeft(1, 0.5)
            stop()
            objectarray=getData()
        forward(1)
  # if the obstacle is to the right, turn the robot left
    elif (objectarray[2]>threshold):
        while (objectarray[2]>threshold):
            stop()

            turnLeft(1, 0.5)
            forward(1, 0.5)
            turnRight(1, 0.5)
            stop()
            objectarrgetData()
        forward(1)




# method that can be implemented to check if there is an object
def checkIfObject():
    if(getObstacle("right") > threshold or getObstacle("center") > threshold or getObstacle("left") > threshold):
        return True;


from myro import *

init("/dev/rfcomm1")
# 0-7000 value for proximity of obstacle
threshold = 100
setIRPower(135)
setName("JMBOT")
forward(1)
#returns an list with the proximity values from  IR sensors
def getData():
    left=getObstacle("left")
    right=getObstacle("right")
    center=getObstacle("center")
    return [left,center,right]

while 1:
    #Debug
    objectarray=getData()
    print str(objectarray[0])+" "+str(objectarray[1])+" "+str(objectarray[2])
    # if the obstacle is left or in the centre, then turn right
    if (isObjectLeft(objectarray)):
        goAroundObject(1);
  # if the obstacle is to the right, turn the robot left
    elif (isObjectRight(objectarray)):
        goAroundObject(2);

    forward(1)



# method that can be implemented to check if there is an object
def checkIfObject():
    #quick check to see if any object
    if(getObstacle("right") > threshold or getObstacle("center") > threshold or getObstacle("left") > threshold):
        return True;
def isObjectLeft(objectarray):
    if(objectarray[1]>threshold or objectarray[0]>threshold):
        return True;
    else return False;
def isObjectRight(objectarray):
    if(objectarray[2]>threshold):
        return True;
    else return False;
def goAroundObject(direction):
    rightcount=0;
    if direction==1:
        #go right around object
        while isObjectLeft(objectarray):
            rightcount++;
            turnRight(1);
            objectarray=getData();
        forward(1);
        while(rightcount>0):
            rightcount--;
            turnLeft(1);
            objectarray=getData()
        forward(1);
    elif direction==2:
        #go left around object
        #go right around object
        while isObjectLeft(objectarray):
            rightcount++;
            turnLeft(1);
            objectarray=getData();
        forward(1);
        while(rightcount>0):
            rightcount--;
            turnRight(1);
            objectarray=getData()
        forward(1);


from myro import *
init("/dev/rfcomm0")
threshold=300
sensordata=[0,0]
angularspeed=360
# returns true if sensors detect an object within a threshold
def isObject():
  getData()
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    return True
#return True if the object is to the left or False if to the right
def whatDir():
  if(sensordata[0]>sensordata[1]):
    return True
  else
    return False
#sets the static sensordata variable to the current obstacle values
def getData()
  sensordata[0]=getObstacle("left")
  sensordata[1]=getObstacle("right")

#main loop of function to run robot

def move():
  if(isObject()):
    direction=whatDir()
    while(isObject()):
      #if the object is to the left
      if(direction):
        turnRight(1.0,degrees*angularspeed)
      #if the object is to the right
      else:
        turnLeft(1.0,degrees*angularspeed)

  else:
    forward()


angularspeed=calibrate();
while (1):
  move()

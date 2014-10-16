from myro import *
import math
import calibration
init("/dev/rfcomm0")
threshold=300 #Threshold for sensor to confirm obstacle
sensordata=[0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed
deviation = [0, 0] #Net vector of all the deviations
app_vector = [0, 0] #Individual vector of a change

# returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    return True

#return True if the object is bigger to the left or False if to the right
def whatDir():
  if(sensordata[0]>sensordata[1]):
    return True
  else
    return False

#sets the static sensordata variable to the current obstacle values
def getData():
  sensordata[0]=getObstacle("left")
  sensordata[1]=getObstacle("right")

#main loop of function to run robot
def move():
  if(isObject()):
    direction=whatDir()
    while(isObject()):
      #if the object is bigger on the left
      if(direction):
        turnRight(1.0, degrees/angularspeed)
        app_vector[0] += degrees
      #if the object is bigger on the right
      else:
        turnLeft(1.0,degrees/angularspeed)
        app_vector[0] -= degrees
  else:
    forward()


angularspeed=calibrate();
while (1):
  move()

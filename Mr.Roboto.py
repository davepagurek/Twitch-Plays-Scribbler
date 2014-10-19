from myro import *
import math
import calibration
init("/dev/rfcomm0")
threshold=300 #Threshold for sensor to confirm obstacle
sensordata=[0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed, value should be degrees/second 
deviation = [0, 0] #Net vector of all the deviations
app_vector = [0, 0] #Individual vector of a displacement
ang_step = 15 #Angular rotation for step in degrees
cleared = False #Boolean to see if obstacle side is cleared

# returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    return True

#return True if the object is bigger to the left or False if to the right
def whatDir():
  if(sensordata[0]>sensordata[1]):
    return True
  else:
    return False

#sets the static sensordata variable to the current obstacle values
def getData():
  sensordata[0]=getObstacle("left")
  sensordata[1]=getObstacle("right")

#makes the bot face a clear path
def directBot():
  direction=whatDir()
    while(isObject()):
      #if the object is bigger on the left
      if(direction):
        turnRight(0.5, ang_step/angularspeed)
        app_vector[0] += ang_step
      #if the object is bigger on the right
      else:
        turnLeft(0.5, ang_step/angularspeed)
        app_vector[0] -= ang_step

#makes the bot clear one side of the obstacle
def clearObs():
  cleared = False
  while (!cleared):
    forward (0.5, 0.5)
    app_vector[1] += 0.5
    #object side is to the left
    if(direction):
      turnLeft(0.5, 90/angularspeed)
      if (!isObject()):
        cleared = True
      turnRight(0.5, 90/angularspeed)
    #object side is to the right
    else:
      turnRight(0.5, 90/angularspeed)
      if (!isObject()):
        cleared = True
      turnLeft(0.5, 90/angularspeed)
  forward (1.0, 0.5)
  app_vector[1] += 0.5
  if(direction):
    turnLeft(0.5, app_vector[0]/angularspeed)
  else:
    turnRight(0.5, -app_vector[0]/angularspeed)

#corrects any displacement performed by the bot
def revert():
  if(app_vector[1]>0):
    if app_vector[0]>0:
      turnLeft(0.5, app_vector[0]/angularspeed)
    else:
      turnRight(0.5, -app_vector[0]/angularspeed)
    forward(0.5, app_vector[1])
  if app_vector[0]>0:
      turnRight(0.5, app_vector[0]/angularspeed)
    else:
      turnLeft(0.5, -app_vector[0]/angularspeed)
  app_vector = [0,0]

#main loop of function to run bot
def move():
  if(isObject()):
    directBot()
    clearObs()
    revert()
  else:
    forward()


angularspeed=calibrate();
while (1):
  move()

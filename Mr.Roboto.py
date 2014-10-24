from myro import *
import math
from Vector import *
from calibration import *
init("/dev/rfcomm1")
threshold=800 #Threshold for sensor to confirm obstacle
sensordata=[0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed, value should be degrees/second
#deviation = [0, 0] #Net vector of all the deviations
deviation =  Vector(0, 0)
#app_vector = [0, 0] #Individual vector of a displacement, [angle, steps]
app_vector = Vector(0, 0)
ang_step = 15 #Angular rotation for step in degrees
cleared = False #Boolean to see if obstacle side is cleared
direction = True
setIRPower(135)
forwardvalue=1
forwardspeed=0.5
turnspeed=0.5



# returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  print sensordata
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    print "saw obstacle"
    return True
  else:
    return False

#return True if the object is bigger to the left or False if to the right
def whatDir():
  if(sensordata[0]>sensordata[1]):
    direction= True
    print "object to left"
  else:
    direction= False
    print "object to right"

#sets the static sensordata variable to the current obstacle values
def getData():
  a=0
  b=0
  for x in range (3):
    a+=getObstacle("left")
    b+=getObstacle("right")
  sensordata[0]=a/3
  sensordata[1]=b/3

#makes the bot face a clear path
def directBot():
  while(isObject()):

    #if the object is bigger on the left
    if(direction):
      turnRight(turnspeed, ang_step/angularspeed)
      app_vector.angle += ang_step
      print ang_step
      #if the object is bigger on the right
    else:
      turnLeft(turnspeed, ang_step/angularspeed)
      app_vector.angle -= ang_step
      print ang_step

#makes the bot clear one side of the obstacle
def clearObs():
  print "clearing obstacle"
  cleared = False
  while (not cleared):
    forward(forwardspeed,forwardvalue)
    app_vector.magnitude += 0.5
    #object side is to the left
    if(direction):
      turnLeft(turnspeed, 90/angularspeed)
      if (not isObject()):
        cleared = True
      turnRight(turnspeed, 90/angularspeed)
    #object side is to the right
    else:
      turnRight(turnspeed, 90/angularspeed)
      if (not isObject()):
        cleared = True
      turnLeft(turnspeed, 90/angularspeed)
  print "cleared obstacle"
  forward (forwardspeed, forwardvalue)
  app_vector.magnitude += 0.5
  if(direction):
    turnLeft(turnspeed, app_vector.angle/angularspeed)
  else:
    turnRight(turnspeed, -app_vector.angle/angularspeed)

#corrects any displacement performed by the bot
def revert():
  if(app_vector.magnitude>0):
    if app_vector.angle>0:
      turnLeft(turnspeed, app_vector.angle/angularspeed)
    else:
      turnRight(turnspeed, -app_vector.angle/angularspeed)
    forward(forwardspeed, app_vector.magnitude)
  if app_vector.angle>0:
    turnRight(turnspeed, app_vector.angle/angularspeed)
  else:
    turnLeft(turnspeed, -app_vector.angle/angularspeed)
  deviation.add(app_vector)
  app_vector.angle = 0.0
  app_vector.magnitude = 0.0

def turnParallel():
  i = 0
  distance_array = []
  while i<=720:
    getData()
    distance_array.push((i,sensordata[0]+sensordata[1]))
    i+=5

#main loop of function to run bot
def move():
  if(isObject()):
    directBot()
    clearObs()
    revert()
  else:
    forward()


angularspeed=calibrate()
while (1):
  move()

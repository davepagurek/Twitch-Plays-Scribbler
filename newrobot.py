from myro import *
import math
from Vector import *
from calibration import *
init("/dev/rfcomm1")
threshold=800 #Threshold for sensor to confirm obstacle
sensordata=[0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed, value should be degrees/second
#deviation = [0, 0] #Net vector of all the deviations
#app_vector = [0, 0] #Individual vector of a displacement, [angle, steps]
ang_step = 90 #Angular rotation for step in degrees
direction = True
setIRPower(135)
forwardvalue=1
forwardspeed=0.5
turnspeed=0.5
xdisplacement=0
#holds angle heading
angle=0
#calibrates robot


# returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  print sensordata
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    return True
  else:
    return False

#return True if the object is bigger to the left or False if to the right
def whatDir():
  if(sensordata[0]>sensordata[1]):
    direction= True
  else:
    direction= False

#sets the static sensordata variable to the current obstacle values
def getData():
  a=0
  b=0
  #gets 3 sets of data to smooth out data
  for x in range (3):
    a+=getObstacle("left")
    b+=getObstacle("right")
  sensordata[0]=a/3
  sensordata[1]=b/3

#makes the bot face a clear path
def directBot():
  global angle
  while(isObject()):
    """if the object is bigger on the left continue to steer the angle away from the object until a clear path is seen"""
    if(direction):
      turnRight(turnspeed, ang_step/angularspeed)
      angle+=ang_step
      #if the object is bigger on the right
    else:
      turnLeft(turnspeed, ang_step/angularspeed)
      angle -= ang_step
  # #add an extra step in case
  # if(direction):
  #   turnRight(turnspeed, ang_step/angularspeed)
  #   angle += ang_step
  # else:
  #   turnLeft(turnspeed, ang_step/angularspeed)
  #   angle -= ang_step


#stays in direction if there isnt an object
def checkIfClear(d):
  if(direction):
    print"turning left to avoid obstacle"
    turnLeft(turnspeed, ang_step/angularspeed)
    angle-=ang_step
    if (not isObject()):
      turnRight(turnspeed, ang_step/angularspeed)
      angle+=angstep
      return True
    else:
      turnRight(turnspeed, ang_step/angularspeed)
      angle+=angstep
      return False

#object side is to the right
  else:
    print "turning right to avoid obstacle"
    angle+=ang_step
    turnRight(turnspeed, ang_step/angularspeed)
    if (not isObject()):
      turnLeft(turnspeed,ang_step/angularspeed)
      angle-=ang_step
      return True
    else:
      turnLeft(turnspeed,ang_step/angularspeed)
      angle-=ang_step
      return False


#main loop of function to run bot
def moveone():
  global xdisplacement
  print (xdisplacement, isObject(), angle)
  if(abs(xdisplacement)>0 or isObject() or angle>0 or angle<0):
    if(isObject()):
      print("avoiding obstacle")
      #sets the variable initially
      whatDir()
      #gets robot to clear path
      directBot()
      forward(1)
      while(checkIfClear()):
      #positice to right, negative to left
        if(direction):
          xdisplacement += 1
        else:
          xdisplacement -= 1
    #if there isnt an object
    else:
      print"no obstacle ... trying to course correct"
      if(not angle<=10 or not angle>=-10):
        returnToOriginAngle()
      if(xdisplacement>0):
        print"had moved right... correcting"
        turnLeft(turnspeed,ang_step/angularspeed)
        forward(1)
        xdisplacement-=1
      elif(xdisplacement.x<0):
        print "moved left... correcting"
        turnRight(turnspeed,ang_step/angularspeed)
        forward(1)
        xdisplacement+=1
  else:
    print"forward"
    forward(1)

def returnToOriginAngle():
  global angle

  while(not angle<=10 or not angle>=-10):
    if(angle>10):
      print"turning left to get back to original angle ",angle
      turnLeft(turnspeed,ang_step/angularspeed)
      angle-=ang_step
    elif(angle<10):
      print"turning right to get back to original angle",angle
      turnRight(turnspeed,ang_step/angularspeed)
      angle+=ang_step
class Robot():
	heading=0
	xdisplacement=0
	ydisplacement=0
	def __init__(self):

	def moveLeft(time):

	def moveRight(time):
angularspeed=calibrate()

while (1):
  moveone()

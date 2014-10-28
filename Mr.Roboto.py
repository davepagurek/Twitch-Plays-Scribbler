from myro import *
import math
from Vector import *
from calibration import *
init("/dev/rfcomm1")
threshold=660 #Threshold for sensor to confirm obstacle
sensordata=[0,0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed, value should be degrees/second
deviation = Vector(0,0) #Net vector of all the deviations
app_vector = Vector(0,0) #Individual vector of a displacement, [angle, steps]
ang_step = 15 #Angular rotation for step in degrees
cleared = False #Boolean to see if obstacle side is cleared
direction = True
#perpendicular = False
setIRPower(135)
forwardvalue=1.25
forwardspeed=0.5
turnspeed=0.5
state = 0

import time
import sys
import select
import tty
import termios
import threading, time

#calibrate the turnspeed of the robot by seeing how long it takes to turn 360 degrees
def calibrate():
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        start = time.time()
        thread = threading.Thread(target=turn).start()

        while 1:
          if isData():
            c = sys.stdin.read(1)
            if c == '\x1b':         # x1b is ESC
              stop()
              end = time.time()
              break

    finally:
      termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
      return 360/(end - start)

def turn():
    turnRight(turnspeed)

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

#tells the robot what type of obstacle avoidance to use (perpendicular or angled)
def set_state():
    temp = input("Enter Mode. 1 for perpendicular. 2 for angled")
    if(not(temp == "1" or temp == "2")) return 0
    return temp

#returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  print sensordata
  if(sensordata[0]>threshold or sensordata[1]>threshold or sensordata[2]>threshold):
    print "Saw obstacle"
    return True
  else:
    return False

#returns true if one of the sensors (left/right) returns a 0 (meaning it's clear or on a border)
def onBorder():
  getData()
  print sensordata
  if(sensordata[0]==0 or sensordata[1]==0):
    print "On a border"
    return False
  else:
    return True

#return True if the object is bigger to the left or False if to the right
def whatDir():
  global direction
  if(sensordata[0]>sensordata[1]):
    direction= True
    print "object to left"
  else:
    direction= False
    print "object to right"

#sets the static sensordata variable to the current obstacle values, takes an average of 3 data sets
def getData():
  a=0
  b=0
  c=0
  for x in range (3):
    a+=getObstacle("left")
    b+=getObstacle("right")
    c+=getObstacle("center")
  sensordata[0]=a/3
  sensordata[1]=b/3
  sensordata[2]=c/3

#makes the bot face a clear path
def directBot():
  global direction
  global state
  #global perpendicular
  # #gets a bit closer to sense object better
  # forward(forwardspeed, 0.3)
  # perpendicular = True
  # turnLeft(turnspeed, 90/angularspeed)
  # if (isObject()):
  #   perpendicular = False
  #   turnRight(turnspeed, 90/angularspeed)
  # else:
  #   forward(forwardspeed, 0.5)
  #   turnRight(turnspeed, 90/angularspeed)
  #   if not (isObject()):
  #     perpendicular = False
  #     turnRight(turnspeed, 90/angularspeed)
  #     forward(forwardspeed, 0.5)
  #     turnLeft(turnspeed, 90/angularspeed)
  #   else:
  #     turnRight(turnspeed, 90/angularspeed)
  #     forward(forwardspeed, 0.5)
  #     if (isObject()):
  #       perpendicular = False
  #       turnLeft(turnspeed, 90/angularspeed)
  #     else:
  #       forward(forwardspeed, 0.5)
  #       turnLeft(turnspeed, 90/angularspeed)
  #       if not (isObject()):
  #         perpendicular = False
  #       turnLeft(turnspeed, 90/angularspeed)
  #       forward(forwardspeed, 0.5)
  #       turnRight(turnspeed, 90/angularspeed)
  #else:
#      forward(forwardspeed, 0.3)

  #Perpendicular direction
  if (state == 1):
    if (direction):
      turnRight(turnspeed, 90/angularspeed)
      app_vector.angle += 90
      print 90
    else:
      turnLeft(turnspeed, 90/angularspeed)
      app_vector.angle -= 90
      print -90
  #Angular direction
  else:
    #turn until no object in path
    while(isObject()):
      #if the object is bigger on the left
      print direction
      if(direction==True):
        turnRight(turnspeed, ang_step/angularspeed)
        app_vector.angle += ang_step
        print ang_step
        #if the object is bigger on the right
      else:
        turnLeft(turnspeed, ang_step/angularspeed)
        app_vector.angle -= ang_step
        print ang_step
    #Plus one more for safety
    if(direction==True):
      turnRight(turnspeed, ang_step/angularspeed)
      app_vector.angle += ang_step
      print ang_step
      print "Last turn"
    else:
      turnLeft(turnspeed, ang_step/angularspeed)
      app_vector.angle -= ang_step
      print ang_step
      print "Last turn"

#makes the bot clear one side of the obstacle
def clearObs():
  global direction
  print "clearing obstacle"
  cleared = False
  #move forward in case too far from obstacle
  forward(forwardspeed, 1.0)
  app_vector.magnitude += 1.0
  #move forward while check to clear obstacle
  while (not cleared):
    forward(forwardspeed,forwardvalue)
    app_vector.magnitude += forwardvalue
    #object side is to the left
    if(direction==True):
      turnLeft(turnspeed, 90/angularspeed)
      if (not onBorder()):
        cleared = True
      turnRight(turnspeed, 90/angularspeed)
    #object side is to the right
    else:
      turnRight(turnspeed, 90/angularspeed)
      if (not onBorder()):
        cleared = True
      turnLeft(turnspeed, 90/angularspeed)
  print "cleared obstacle"
  forward (forwardspeed, forwardvalue)
  app_vector.magnitude += forwardvalue
  if(direction==True):
    turnLeft(turnspeed, app_vector.angle/angularspeed)
  else:
    turnRight(turnspeed, -app_vector.angle/angularspeed)

#corrects any displacement performed by the bot
def revert():
  global direction
  global state
  #set deviation vector to the complimentary angle
  if app_vector.angle>0:
    deviation.angle = 90 - app_vector.angle
  else:
    deviation.angle = - 90 - app_vector.angle
  #set deviation vector to the corresponding magnitude
  if (state == 1):
    deviation.magnitude = app_vector.magnitude
  else:
    deviation.magnitude = math.fabs(app_vector.magnitude*math.cos((deviation.angle/180)*math.pi)/math.cos((app_vector.angle/180)*math.pi))
  #turn to deviation angle
  if deviation.angle>0:
    turnLeft(turnspeed, deviation.angle/angularspeed)
  else:
    turnRight(turnspeed, -deviation.angle/angularspeed)
  #moves in the deviation vector and resets all vectors
  print deviation.magnitude,"\n\n\n", forwardspeed
  forward(forwardspeed, int(deviation.magnitude))
  if deviation.angle>0:
    turnRight(turnspeed, deviation.angle/angularspeed)
  else:
    turnLeft(turnspeed, -deviation.angle/angularspeed)
  deviation.angle = 0
  deviation.magnitude = 0
  app_vector.angle = 0
  app_vector.magnitude = 0

 #perpendicular avoidance clearing side of box
def moveL():
  global direction
  cleared = False
  #move forward in case box is too far
  forward(forwardspeed, 2)
  #move forward until box is cleared
  while (not cleared):
    forward(forwardspeed,forwardvalue)
    #object side is to the left
    if(direction==True):
      turnLeft(turnspeed, 90/angularspeed)
      if (not onBorder()):
        cleared = True
      turnRight(turnspeed, 90/angularspeed)
    #object side is to the right
    else:
      turnRight(turnspeed, 90/angularspeed)
      if (not onBorder()):
        cleared = True
      turnLeft(turnspeed, 90/angularspeed)
  forward (forwardspeed, forwardvalue)
  if(direction==True):
    turnLeft(turnspeed, app_vector.angle/angularspeed)
  else:
    turnRight(turnspeed, -app_vector.angle/angularspeed)
  #return to the main axis by reverting the change, reset vectors
  forward (forwardspeed, app_vector.magnitude)
  #return forward
  if(direction==True):
    turnRight(turnspeed, app_vector.angle/angularspeed)
  else:
    turnLeft(turnspeed, -app_vector.angle/angularspeed)
  app_vector.angle = 0
  app_vector.magnitude =0

#main loop of function to run bot
def move():
  global direction
  if(isObject()):
    whatDir()
    print direction
    directBot()
    clearObs()
    print app_vector.angle
    if (app_vector.angle > 80.0 or app_vector.angle < -80.0):
        moveL()
    else:
        revert()
  else:
    forward(1, 0.25)

angularspeed=calibrate()
state = set_state()
while (1):
  move()

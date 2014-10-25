from myro import *
import math
from Vector import *
from calibration import *
init("/dev/rfcomm1")
threshold=550 #Threshold for sensor to confirm obstacle
sensordata=[0,0] #Holds sensor data for obstacles (Left, Right)
angularspeed=360 #Need to set to calibrated angular speed, value should be degrees/second
deviation = Vector(0,0) #Net vector of all the deviations
app_vector = Vector(0,0) #Individual vector of a displacement, [angle, steps]
ang_step = 15 #Angular rotation for step in degrees
cleared = False #Boolean to see if obstacle side is cleared
direction = True
setIRPower(135)
forwardvalue=1
forwardspeed=0.5
turnspeed=0.5

import time
import sys
import select
import tty
import termios
import threading, time
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

# returns true if sensors detect an object greater than a threshold
def isObject():
  getData()
  print sensordata
  if(sensordata[0]>threshold or sensordata[1]>threshold):
    print "saw obstacle"
    return True
  else:
    return False

def onBorder():
  getData()
  print sensordata
  if(sensordata[0]>threshold and sensordata[1]>threshold):
    print "saw obstacle"
    return True
  else:
    return False

#return True if the object is bigger to the left or False if to the right
def whatDir():
  global direction
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
  global direction
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
    if (app_vector.angle == 75):
        break
  #correct back to 90 degrees
  """if (app_vector.angle == 75):
      if(direction==True):
        turnRight(turnspeed, 30/angularspeed)
        app_vector.angle += 30
        print ang_step
        #if the object is bigger on the right
      else:
        turnLeft(turnspeed, 30/angularspeed)
        app_vector.angle -= 30
        print ang_step
  #extra step for error just in case
  else:
      if(direction==True):
        turnRight(turnspeed, ang_step/angularspeed)
        app_vector.angle += ang_step
        print ang_step
      else:
        turnLeft(turnspeed, ang_step/angularspeed)
        app_vector.angle -= ang_step
        print ang_step"""
  if(direction==True):
    turnRight(turnspeed, ang_step/angularspeed)
    app_vector.angle += ang_step
    print ang_step
  else:
    turnLeft(turnspeed, ang_step/angularspeed)
    app_vector.angle -= ang_step
    print ang_step

#makes the bot clear one side of the obstacle
def clearObs():
  global direction
  print "clearing obstacle"
  cleared = False
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
  #set deviation vector to the complimentary angle
  if app_vector.angle>0:
    deviation.angle = 90 - app_vector.angle
  else:
    deviation.angle = - 90 - app_vector.angle
  #set deviation vector to the corresponding magnitude
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

 #function to clear box from the side
def moveL():
  global direction
  cleared = False
  forward(forwardspeed, 2)
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
  forward (forwardspeed, app_vector.magnitude)
  #return forward
  if(direction==True):
    turnRight(turnspeed, app_vector.angle/angularspeed)
  else:
    turnLeft(turnspeed, -app_vector.angle/angularspeed)
  app_vector.angle = 0
  app_vector.magnitude =0

'''def turnParallel():
  i = 0
  distance_array = []
  while i<=720:
    getData()
    #distance_array.push((i,sensordata[0]+sensordata[1]))
    i+=5
  max_val_1 = max(lis[0:360],key=lambda item:item[1])
  max_val_2 = max(lis[360:720],key=lambda item:item[1])
  print (max_val_1)
  print (max_val_2)'''

#main loop of function to run bot
def move():
  global direction
  #turnParallel()
  if(isObject()):
    whatDir()
    print direction
    directBot()
    clearObs()
    if (app_vector.angle == 90 or app_vector == -90):
        moveL()
    else:
        revert()
  else:
    forward()


angularspeed=calibrate()
while (1):
  move()

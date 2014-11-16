import logging
import json
import threading
import sched, time
from cv2 import *
import playsampledictionary
logging.basicConfig(level=logging.ERROR)
from socketIO_client import SocketIO
import pdb
import random
robot = True

if (robot):
  from myro import *
  init("/dev/rfcomm0")

queue = []
ready = True
idle = True
s = sched.scheduler(time.time, time.sleep)



with SocketIO("scribblerplaystwitch.herokuapp.com") as socket:

  def start_executer():
    global ready
    global s
    while (1):
      if (ready):
        apply_command()
      else:
        time.sleep(0.1)

  def apply_command():
    global queue
    global s
    global ready
    global idle
    if len(queue)>0:
      ready = False
      idle = False
      snum=random.randint(0,len(queue)-1);
      selected = queue.pop(snum)
      queue = []
      command = selected["message"].lower()
      print command
      username = selected["username"]
      if (not robot):
        time.sleep(2)
      else:
        if(command=="forward" or command=="straight"):
          forward(1,1)
        elif(command=="backward" or command=="back"):
          backward(1,1)
        elif(command=="right"):
          turnRight(1,0.5)
        elif(command=="left"):
          turnLeft(1,0.5)
        elif(command=="spin"):
           turnRight(1,3)
        elif(command=="hasselhoff"):
          playsampledictionary.playHookedOnAFeeling()
        elif(command=="beep"):
          beep(1,440*5)
      take_photo()
      socket.emit("selected", {'username': username, 'message': command})
      #time.sleep(2)
      ready = True

  def take_photo():
    if (robot):
      picture = takePicture("color")
      savePicture(picture, "static/stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
    image_file.close()

  def webcam_photo():
    global cam
    cam = VideoCapture(0)
    cam.set(3,256)
    cam.set(4,192)
    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
    while (1):
      s, img = cam.read()
      if s:    # frame captured without any errors

        imshow("cam-test",img)
        #time.sleep(2)
        #destroyWindow("cam-test")
        cv.SaveImage("static/webcam.jpg", cv.fromarray(img))
        waitKey(200)

      image_file = open("static/webcam.jpg", "rb")
      data = image_file.read()
      socket.emit("webcam", data.encode("base64"))
      image_file.close()

  def valid_command(command):
    command = command.lower()
    if (command=="forward" \
    or command=="backward" \
    or command =="straight" \
    or command =="back" \
    or command =="spin" \
    or command=="right" \
    or command=="left" \
    or command =="spin" \
    or command=="hasselhoff" \
    or command=="beep"):
      return True
    else:
      return False

  def on_command(*args):
    global queue
    if (valid_command(args[0]["message"])):
      queue.append(args[0])

  if (robot):
    executer = threading.Thread(target=start_executer, args = ())
    executer.daemon = True
    executer.start()

  webcam = threading.Thread(target=webcam_photo, args = ())
  webcam.daemon = True
  webcam.start()

  socket.on("command", on_command)
  #socketer = threading.Thread(target=socket.wait, args = ())
  #socketer.daemon = True
  #socketer.start()
  socket.wait()

  #if (not robot):
  #webcam_photo()

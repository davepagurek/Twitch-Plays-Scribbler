import logging
import json
import threading
import sched, time
from cv2 import *
import playsampledictionary
logging.basicConfig(level=logging.ERROR)
from socketIO_client import SocketIO

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
      selected = queue.pop(0)
      queue = []
      command = selected["message"]
      username = selected["username"]
      if (not robot):
        time.sleep(2)
      else:
        if(command=="forward"):
          forward(1,1)
        elif(command=="backward"):
          backward(1,1)
        elif(command=="right"):
          turnRight(1,1)
        elif(command=="left"):
          turnLeft(1,1)
        elif(command=="beep"):
          song()
        elif(command=="hasselhoff"):
          speak("Im hooked on a feeling")
          playsampledictionary.playHookedOnAFeeling()

      print "this is how we do"
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
        waitKey(42)

      image_file = open("static/webcam.jpg", "rb")
      data = image_file.read()
      socket.emit("webcam", data.encode("base64"))
      image_file.close()

  def valid_command(command):
    if (command=="forward" or command=="backward" or command=="right" or command=="left" or command=="hasselhoff" or command=="beep"):
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
  while 1:
      socket.wait()

  #if (not robot):
  #webcam_photo()

import logging
import json
import threading
import sched, time
#import pygame.camera
#import pygame.image
#from SimpleCV import Image, Camera
from cv2 import *
#import song
logging.basicConfig(level=logging.WARNING)
from socketIO_client import SocketIO

dev = True

if (not dev):
  #from myro import *
  init("/dev/rfcomm1")

queue = []
ready = True
idle = True
s = sched.scheduler(time.time, time.sleep)
#pygame.camera.init()
#cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
#cam.start()


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
      if (dev):
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

      take_photo()
      socket.emit("selected", {'username': username, 'message': command})
      #time.sleep(2)
      ready = True

  def take_photo():
    if (not dev):
      picture = takePicture("color")
      savePicture(picture, "static/stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
    image_file.close()

  def webcam_photo():
    #global cam
    cam = VideoCapture(0)
    while (1):
      time.sleep(2)
      '''img = cam.getImage()
      img.save("static/webcam.jpg")'''

      s, img = cam.read()
      print s
      if s:    # frame captured without any errors
        namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
        imshow("cam-test",img)
        waitKey(0)
        destroyWindow("cam-test")
        imwrite("filename.jpg",img)

      image_file = open("static/webcam.jpg", "rb")
      data = image_file.read()
      socket.emit("webcam", data.encode("base64"))
      image_file.close()

      '''time.sleep(2)
      if (cam.query_image()):
        img = cam.get_image()
        print img
        pygame.image.save(img, "static/webcam.jpg")
        image_file = open("static/webcam.jpg", "rb")
        data = image_file.read()
        socket.emit("webcam", data.encode("base64"))
        image_file.close()'''

  def valid_command(command):
    if (command=="forward" or command=="backward" or command=="right" or command=="left" or command=="hasselhoff" or command=="beep"):
      return True
    else:
      return False

  def on_command(*args):
    global queue
    if (valid_command(args[0]["message"])):
      queue.append(args[0])

  #pygame.camera.quit()

  executer = threading.Thread(target=start_executer, args = ())
  executer.daemon = True
  executer.start()

  webcam = threading.Thread(target=webcam_photo, args = ())
  webcam.daemon = True
  webcam.start()

  socket.on("command", on_command)
  socket.wait()

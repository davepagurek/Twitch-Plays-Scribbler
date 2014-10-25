import logging
import json
import threading
import sched, time
logging.basicConfig(level=logging.WARNING)
from socketIO_client import SocketIO

from myro import *

queue = []
ready = True
idle = True
s = sched.scheduler(time.time, time.sleep)

init("/dev/rfcomm1")
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
      if(command=="forward"):
        forward(1,1)
      elif(command=="backward"):
        backward(1,1)
      elif(command=="right"):
        turnRight(1,1)
      elif(command=="left"):
        turnLeft(1,1)
      elif(command=="beep"):
        beep(1, 87.31)
      elif(command=="hasselhoff"):
        speak("Im hooked on a feeling")
      take_photo()
      socket.emit("selected", {'username': username, 'message': command})
      #time.sleep(2)
      ready = True

  def take_photo():
    picture = takePicture("color")
    savePicture(picture, "static/stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
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

  executer = threading.Thread(target=start_executer, args = ())
  executer.daemon = True
  executer.start()

  socket.on("command", on_command)
  socket.wait()

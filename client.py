import logging
import json
import sched, time
logging.basicConfig(level=logging.DEBUG)
from socketIO_client import SocketIO
from myro import *

queue = []
ready = True
s = sched.scheduler(time.time, time.sleep)

init("/dev/rfcomm1")
with SocketIO("scribblerplaystwitch.herokuapp.com") as socket:

  def check_ready():
    if (ready):
      apply_command()
    else:
      s.enter(0.1, 1, check_ready, ())
      s.run()

  def apply_command():
    ready = False
    selected = random.choice(queue)
    queue = []
    command = selected["message"]
    user = selected["username"]
    if(command=="forward"):
      forward(1,1)
    elif(command=="backward"):
      backward(1,1)
    elif(command=="right"):
      turnRight(1,1)
    elif(command=="left"):
      turnLeft(1,1)
    elif(command=="hasselhoff"):
      speak("Im hooked on a feeling")
    take_photo()
    socket.emit("selected", {'username': username, 'message': command})
    ready = True
    s.enter(0.1, 1, check_ready, ())
    s.run()

  def take_photo():
    print("pretend we're taking a picture")
    picture = takePicture("color")
    savePicture(picture, "static/stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
    image_file.close()

  def on_command(*args):
    #print 'Command sent: ', args
    #do command
    #print "\n\n\n\n"
    #command=args[0]["message"]
    #user=args[0]["username"]
    #print command
    #print "\n\n\n\n\n"
    queue.append(args[0])
    if (ready):
      apply_command()



  socket.on("command", on_command)
  socket.wait()

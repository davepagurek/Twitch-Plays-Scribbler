import logging
import json
logging.basicConfig(level=logging.DEBUG)
from socketIO_client import SocketIO
from myro import *

init("/dev/rfcomm1")
with SocketIO("scribblerplaystwitch.herokuapp.com") as socket:



  def take_photo():
    print("pretend we're taking a picture")
    picture = takePicture("color")
    savePicture(picture, "static/stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
    image_file.close()

  def on_command(*args):
      print 'Command sent: ', args
      #do command
      print args[0]
      print args[1]
      command=args[0]
      if(command=="forward"):
          forward(1)
      elif(command=="backward"):
          backward(1)
      elif(command=="right"):
          turnRight(1,1)
      elif(command=="left"):
          turnLeft(1,1)
      elif(command=="hasselhoff"):
          speak("Im hooked on a feeling")
      socket.emit("selected",dict(username=))
  socket.on("command", on_command)
  socket.wait()
  def switchCommand(command):
    switch

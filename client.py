import logging
import urllib
logging.basicConfig(level=logging.DEBUG)
from socketIO_client import SocketIO

portPage = urllib.urlopen("http://scribblerplaystwitch.herokuapp.com/port")
port = int(portPage.readline() )

print port;

with SocketIO("scribblerplaystwitch.herokuapp.com", port) as socket:

  #from myro import *

  #init("/dev/rfcomm1")

  def take_photo():
    print("pretend we're taking a picture")
    #picture = takePicture("color")
    #savePicture(picture, "stream.jpg")
    image_file = open("static/stream.jpg", "rb")
    data = image_file.read()
    socket.emit("photo", data.encode("base64"))
    image_file.close()

  def on_command(*args):
      print 'Command sent: ', args
      #do command
      take_photo()

  socket.on("command", on_command)
  socket.wait()
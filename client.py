from socketio_client import SocketIOClient
import base64

#socket = SocketIOClient("localhost", 8000)

#from myro import *

#init("/dev/rfcomm1")

def take_photo():
	print("pretend we're taking a picture")
	#picture = takePicture("color")
	#savePicture(picture, "stream.jpg")
	image_file = open("stream.jpg", "rb")
	data = image_file.read()
	socket.emit("photo", data.encode("base64"))
	image_file.close()

def on_command(*args):
    print 'Command sent: ', args
    #do command
    take_photo()

def on_connect():
    print("opened!")
    socket.on("command", on_command)

socket.on("connect", on_connect)
socket.run()

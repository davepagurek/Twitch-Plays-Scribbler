from cv2 import *

def webcam_photo():
  #global cam
  cam = VideoCapture(0)
  while (1):
    #time.sleep(2)
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
    #socket.emit("webcam", data.encode("base64"))
    image_file.close()

webcam_photo()
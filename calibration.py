from myro import*

init("/dev/rfcomm0")

import time
import sys
import select
import tty
import termios
import threading, time

def calibrate():

  def turn():
      print "robot turning at speed .5 \n"
      turnRight(.5, 1000)
      print "robot stop turning\n"
  print "Please press ESC when the robot turns 360 degrees\n"


  def isData():
      return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

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
      print str(end - start) + "| Angular speed: " + str((end - start)/360)
      return (end - start)/360

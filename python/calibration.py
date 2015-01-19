import time
import sys
import select
import tty
import termios
import threading, time
from myro import *
turnspeed=0.5
def calibrate():
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
      return 360/(end - start)
def turn():
    turnRight(turnspeed)

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

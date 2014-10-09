import myro
import time
import sys
import select
import tty
import termios
import threading, time

def turn():
    print "robot turning\n"
    turnRight(.5, 1000)
    print "robot stop turning\n"
print "Please press a button when robot turns 360 degrees\n"


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    i = 0
    start = time.time()
    thread = threading.Thread(target=turn).start()

    while 1:
            print i
            i += 1
            if isData():
                    c = sys.stdin.read(1)
                    if c == '\x1b':         # x1b is ESC
                            stop()
                            end = time.time()
                            break

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print "Time: " + end - start

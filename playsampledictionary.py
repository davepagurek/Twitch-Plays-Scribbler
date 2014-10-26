from myro import *
init("/dev/rfcomm1")
from audiojm import *
j=audiojm()
notearray=[Note(1,audiojm.A5),Note(1,audiojm.A4)]
j.playNoteDictionary(notearray)

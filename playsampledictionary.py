from myro import *
init("/dev/rfcomm1")
from audiojm import *
j=audiojm()
notearray=[Note(0.2,audiojm.B4),Note(0.4,audiojm.D5),Note(0.4,audiojm.D5),Note(0.4,audiojm.D5),Note(0.4,audiojm.E5),Note(3.5*0.4,audiojm.D5)]
j.playNoteDictionary(notearray)

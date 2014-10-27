from Myro import *
init("/dev/rfcomm1")
from audiojm import *
j=audiojm()
melody=[Note(0.2,audiojm.B4),Note(0.4,audiojm.D5),Note(0.4,audiojm.D5),Note(0.4,audiojm.D5),Note(0.4,audiojm.E5),Note(3.5*0.4,audiojm.D5),Note(0.2,audiojm.B4),Note(0.4,audiojm.D5),Note(0.2,audiojm.E5),Note(0.4,audiojm.D5),Note(0.2,audiojm.C5),Note(4.5*0.4,audiojm.C5),Note(1.5*0.4,audiojm.C5),Note(0.4,audiojm.D5),Note(0.4,audiojm.C5),Note(0.4*3.5,audiojm.B4),Note(0.4*0.5,audiojm.A4),Note(0.4*0.5,audiojm.G4),Note(0.4*0.5,audiojm.B4),Note(0.4*0.5,audiojm.G4),Note(0.4*6,audiojm.A4)]
harmony=[Note(0.4*11,audiojm.G4),Note(0.4*3,audiojm.FS4),Note(0.4*2,audiojm.D4),Note(0.4*3.5,audiojm.FS4),Note(0.4*3.5,audiojm.D4),Note(0.4,audiojm.A3),Note(0.4*7,audiojm.D4)]
j.playNoteDictionary(melody, harmony)

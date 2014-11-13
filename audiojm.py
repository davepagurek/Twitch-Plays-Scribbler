from myro import *
class audiojm():
    B0  = 31
    C1  = 33
    CS1 = 35
    D1  = 37
    DS1 = 39
    E1  = 41
    F1  = 44
    FS1 = 46
    G1  = 49
    GS1 = 52
    A1  = 55
    AS1 = 58
    B1  = 62
    C2  = 65
    CS2 = 69
    D2  = 73
    DS2 = 78
    E2  = 82
    F2  = 87
    FS2 = 93
    G2  = 98
    GS2 = 104
    A2  = 110
    AS2 = 117
    B2  = 123
    C3  = 131
    CS3 = 139
    D3  = 147
    DS3 = 156
    E3  = 165
    F3  = 175
    FS3 = 185
    G3  = 196
    GS3 = 208
    A3  = 220
    AS3 = 233
    B3  = 247
    C4  = 262
    CS4 = 277
    D4  = 294
    S4 = 311
    E4  = 330
    F4  = 349
    FS4 = 370
    G4  = 392
    GS4 = 415
    A4  = 440
    AS4 = 466
    B4  = 494
    C5  = 523
    CS5 = 554
    D5  = 587
    DS5 = 622
    E5  = 659
    F5  = 698
    FS5 = 740
    G5  = 784
    GS5 = 831
    A5  = 880
    AS5 = 932
    B5  = 988
    C6  = 1047
    CS6 = 1109
    D6  = 1175
    DS6 = 1245
    E6  = 1319
    F6  = 1397
    FS6 = 1480
    G6  = 1568
    GS6 = 1661
    A6  = 1760
    AS6 = 1865
    B6  = 1976
    C7  = 2093
    CS7 = 2217
    D7  = 2349
    DS7 = 2489
    E7  = 2637
    F7  = 2794
    FS7 = 2960
    G7  = 3136
    GS7 = 3322
    A7  = 3520
    AS7 = 3729
    B7	= 3951
    C8  = 4186
    CS8 = 4435
    D8  = 4699
    DS8 = 4978
    duration=0.1
    def setDuration(self,duration):
        self.duration=duration
    def playNote(self,note):
        beep(0.1,note)
    def playNoteDictionary(self, melody, harmony):
        arpeggiate = False
        currentMelody = None
        currentHarmony = None
        arpLength = 0.1
        while (len(melody)>0 or len(harmony)>0):
            if (len(harmony)==0 and (not currentHarmony or currentHarmony.played>=currentHarmony.duration)):
                currentMelody = melody.pop(0)
                beep(currentMelody.duration,currentMelody.note)
            elif (len(melody)==0 and (not currentMelody or currentMelody.played>=currentMelody.duration)):
                currentHarmony = harmony.pop(0)
                beep(currentHarmony.duration,currentHarmony.note)
            else:
                if (not currentMelody or currentMelody.played>=currentMelody.duration):
                    currentMelody = melody.pop(0)
                if (not currentHarmony or currentHarmony.played>=currentHarmony.duration):
                    currentHarmony = harmony.pop(0)
                length = min(currentMelody.duration-currentMelody.played, currentHarmony.duration-currentHarmony.played)
                currentMelody.played += length
                currentHarmony.played += length
                if (arpeggiate):
                    x = 0
                    while (x*arpLength<length):
                        x += 1
                        if (x % 2 == 0):
                            beep(arpLength,currentMelody.note)
                        else:
                            beep(arpLength,currentHarmony.note)
                elif (length>0.0001):
                    #print(currentMelody.note, " ", currentHarmony.note)
                    beep(length, currentMelody.note*2, currentHarmony.note*2)

class Note():
    def __init__(self, duration,note):
        self.duration=duration
        self.note=note
        self.played=0

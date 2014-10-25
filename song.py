from myro import*

init("/dev/rfcomm0")

def song():  
    do=523.25
    re=587.33
    mi=659.25
    fa=698.46
    sol=783.99
    la=880.00
    si=987.77
    do2=1046.50
    re2=1174.66
    mi2=1318.51
    fa2=1396.91
    sol2=1567.98

    beep(0.375, sol) 
    beep(0.125, sol) 

    beep(0.5, la)
    beep(0.5, sol) 
    beep(0.5, do2) 

    beep(1, si)
    beep(0.375, sol)
    beep(0.125, sol)

    beep(0.5, la)
    beep(0.5, sol)
    beep(0.5, re2)

    beep(1, do2)
    beep(0.375, sol)
    beep(0.125, sol)

    beep(0.5, sol2)
    beep(0.5, mi2)
    beep(0.5, do2)

    beep(0.5, si)
    beep(0.7, la)
    beep(0.375, fa2)
    beep(0.125, fa2)

    beep(0.5, mi2)
    beep(0.5, do2)
    beep(0.5, re2)
    beep(2, do2)

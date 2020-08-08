import time

def iinput(showstring,default):
    ttemp = input(showstring)
    if ttemp == "":
        return default
    else:
        return ttemp

def fastdivision(value):
    A = ((value + D) * mult) >> N
    return A

def getsizeof(value):
    sizeof = 0
    while value:
        value >>= 1
        sizeof += 1
    return sizeof  

def show_opener():
    print(" ")
    print(" ")
    print(" ")
    print("          |--------------------------- G A N Z Z A H L D I V I S I O N    M I T    A V R - M I K R O C O N T R O L L E R N ------------------------------|")
    print("          |                                                                                                                                              |")
    print("          |   Einfache Mikrocontroller ohne Hardwareunterstützung für Division benötigen sehr viel Rechenzeit zur Ausführung einer Ganzzahldivision.     |")
    print("          |                      ATmega MCUs besitzen im Gegensatz zu ATtiny MCUs eine Hardwareunterstützung für Multiplikation.                         |")
    print("          |   Dieses Script hilft bei der Umwandlung einer Ganzzahldivision in eine inverse Multiplikation mit anschließender Rechtsschiebeoperation,    |")
    print("          |                                     die von allen MCUs einfach und schnell ausgeführt werden kann.                                           |")
    print("          |                                                                                                                                              |")
    print("          |                                                                                                                                              |")
    print("          |                                          aus   A = B // C  mache   A = ((B + D) * (1<<N)//C) >> N                                            |")
    print("          |                                                                                                                                              |")
    print("          |        Da Ganzzahldivisionen immer abrunden erhöht man bei Bedarf für bessere Annäherung an eine Festkommadivision den Dividenten            |")
    print("          |                                                  zusätzlich um die Hälfte des Divisors:                                                      |")
    print("          |                                                                                                                                              |")
    print("          |                                                             B = B + (C >> 1)                                                                 |")
    print("          |                                                                                                                         25mmHg 24.09.2016    |")
    print("          |----------------------------------------------------------------------------------------------------------------------------------------------|")
    print(" ")
    print(" ")

def show_inputdialog():
    global Bmax
    global Bmin
    global C
    global Dmax
    global Dmin
    global Smax
    global Emax
    global Fmax
    global Nmax
    print(" ")
    Bmax = int(iinput("                  größte Zahl, die geteilt werden soll (Dividend): ", 511))
    print("                                                                        Bmax = ", Bmax)
    Bmin = int(iinput("       optional kleinste Zahl, die geteilt werden soll (Dividend): ", 0))
    print("                                                                        Bmin = ", Bmin)
    C    = int(iinput("                     Zahl durch die geteilt werden soll (Divisor): ", 60))
    print("                                                                           C = ", C)
    Dmax = int(iinput("                       optional maximaler Korrekturwert (Summand): ", C // 2 + 1))
    print("                                                                        Dmax = ", Dmax)
    Dmin = int(iinput("                       optional minimaler Korrekturwert (Summand): ", -Dmax))
    print("                                                                        Dmin = ", Dmin)
    Smax = int(iinput("                    optional maximale Streuung des Multiplikators: ", 1))
    print("                                                                        Smax = ", Smax)
    print("                                                                        Smin = ", -Smax)
    Emax = int(iinput("       optional maximale Größe der Abweichung für Anzeige (Error): ", 1))
    print("                                                                        Emax = ", Emax)
    Fmax = int(iinput("     optional maximale Anzahl der Abweichungen über Bmax bis Bmin: ", 22))
    print("                                                                        Fmax = ", Fmax)
    Nmax = int(iinput("                           (größtmögliche) Bitschiebeweite (1<<N): ", 32))
    print("                                                                        Nmax = ", Nmax)
    print(" ")


def show_table():
    print(" ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- ")
    print(" ALLE  ANZAHL  MULTIPLIKATOR                        FEHLERHAFTE                                                                                                          ")
    print(" OK?   FEHLER  ((1<<N)//C)+j  N     D    sizeof()   ERGEBNISSE bei B =                                                                                                   ")
    print(" ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- ")      

def getabsdelta(value):
    A01 = value // C
    A1 = fastdivision(value)
    return abs(A1-A01)

def show_solution():
    print(" %2s   %2i    %#12x     %2i  %3i     %2iBit     %s " % (ok,errcnt,mult,N,D,maxbits,str(falselist)))

show_opener()
while input("                                          Neue Berechnung starten? ") == "ja":
    show_inputdialog()
    oldtime = time.clock()
    for i in range(Nmax,0,-1):
        N = i
        Nold = 0
        for j in range(Smax,-(Smax+1),-1):
            mult = ((1<<N)//C)+j
            if mult < 2:
                break
            for k in range(Dmax,Dmin-1,-1):
                D = k
                ready2print = True
                falselist = []
                errcnt = 0
                ok = "JA "
                maxbits = getsizeof((Bmax + D) * mult)
                for l in range(Bmax, Bmin -1, -1): 
                    B = l
                    absdelta = getabsdelta(B)
                    if absdelta >  Emax:
                        ready2print = False
                        break
                    elif absdelta != 0:
                        ok = "---"
                        falselist.append(B)
                        errcnt = len(falselist)
                        if errcnt > Fmax:
                            ready2print = False
                            break
                if ready2print == True:        
                    if Nold != N:
                        Nold = N
                        show_table()    
                    show_solution()                
    print(" ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- ")
    calctime = time.clock() - oldtime
    print(" Rechenzeit = %6fs" % (calctime))  
    print(" ") 
print(" ")   
print(" >>> ENDE <<<")
time.sleep(3)

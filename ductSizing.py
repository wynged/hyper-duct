import math
import timeit

print("--RUN--DuctSizing")

TestDiam = 972 

def calcEquivalentDiameter(a, b):
    ed = 1.3*(a*b)**0.625/(a+b)**0.25
    return ed

def calcSecondDimension(ed, a, errorFactor=1.5):
    #print "-CALC-ED:{0},A={1}".format(ed, a)
    b = math.pi*(a/2)**2/a
    prevED = calcEquivalentDiameter(a,b)
    error = prevED-ed
    numCalcs = 0
    while abs(error)>.1:# and numCalcs < 20:
        numCalcs = numCalcs+1
        if error<0:
            b = b-error*errorFactor
        elif error>0:
            b = b+error*errorFactor
        newED = calcEquivalentDiameter(a,b)
        error = newED-ed
        prevED = newED
    #print "{0}: B={1}  ED={2}  ERR={3}".format(numCalcs, b, newED, error)
    #print 'NewSize: {0:>5}" x {1:.2f}"'.format(a,b)    
    return b

def calcEDofPDandFlow(flow, pd):
    #flow must be in CFM
    #pd must be in inWC/100ft
    de = ((0.109136*flow**1.9)/pd)**(1/5.02)
    return de

def calcEDofVelAndFlow(flow, vel):
    size = flow / vel
    return size


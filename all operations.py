# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

import numpy as np
from visa import ResourceManager
from scipy import optimize as op

cont_test = np.array([12,23,34,41,13,24])
cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
cont_Rb = np.array([[23,41],[32,14],[41,23],[14,32]]) #Both of these require ADVANCED indexing
cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])

## OR
#cont_Ra = np.array([[43,34,12,21],[21,21,43,43]])
#cont_Rb = np.array([[23,32,41,14],[41,41,32,32]])
I = float(input("Current: "))
N = int(round(float(input("Sampling Count: "))))
t = float(input("thickness (um): "))

def set_up():
    addr = ["GPIB0::3::0::INSTR","GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"]
    rm = ResourceManager()
    instrs = []
    for x in range(0,4):
        instrs.append(rm.open_resource(addr[x], read_termination = "\n"))
    return instrs

def initialise(I,instrs):
    instrs[2].write('A') #set current mode to AC (set "D" for DC but redundant)
    instrs[1].write('SO') #not sure what this does to the instrument but it's needed
    curr = "I"+str(I) #create and stringify current message using out current argument
    instrs[2].write(curr) #send our desired current
    instrs[3].write('G0') #set gain G = 0
    instrs[3].write('H255') #set gain H = 255
    
def meas(N, cont, instrs):
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
#    arr_R = np.empty([len(cont),N]) #same for resistance
    for x in range(0,len(cont)):
        S = "S"+str(cont[x]) #make and stringify source contact probe setting
        M = "M"+str(cont[x]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[3].read() #read volatage in to some variable, insert to our arrays
            arr_I[(x,y)] = instrs[2].read() #read current in to some variable
    return arr_V, arr_I

def gain(Vt,instrs):
    instrs[1].write("S12") #set source contact probes
    instrs[1].write("M34") #set measurement contact probes
    V = abs(Vt/(float(instrs[3].read())/(256/255))) #read volatage in to some variable, insert to our arrays
    if V <= 10:
        return 0, 255/V #V UNSURE THIS DOESN'T WORK {G=1, 255/V} works or {G=0, H = 25.5*V}
    elif V> 10 and V < 100:
        return 1, 2550/V
    elif V >= 100 and V < 1000:
        return 2, 25500/V
    elif V >= 1000 and V < 255000:
        return 3, 255000/V
    else:
        print ("error in gain determination")

def meas_vdp(N, cont, instrs,G):
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
#    arr_R = np.empty([len(cont),N]) #same for resistance
    for x in range(0,len(cont)):
        S = "S"+str(cont[x,0]) #make and stringify source contact probe setting
        M = "M"+str(cont[x,1]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[3].write("G"+str(G[0]))
            instrs[3].write("H"+str(G[1]))
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[2].read() #read voltage in, insert to our arrays
            arr_I[(x,y)] = instrs[1].read() #read current in
    return arr_V, arr_I

#def avg (arr, N):
#    av=np.empty(len(arr),dtype=float)
#    sd=np.empty(len(arr),dtype=float)
#    for i in range (0,len(arr)):
#        av[i] = np.mean(arr[i])
#        sd[i] = np.std(arr[i])
#    return av, sd
#    
#def R (V, I, V_sd, I_sd):
#    R = V/I
#    SDi = V_sd/I_sd
#    Rav = np.mean(R)
#    SDf = np.std(R)
#    return Rav,SDf,R,SDi
#
#def VdP (x, Ra, Rb):
#    pi = -np.pi
#    f = np.exp(pi*Ra/x)+np.exp(pi*Rb/x)-1
#    return f
#
#def VdP_1 (x, Ra, Rb):
#    pi = np.pi
#    f = pi*(Ra*np.exp(-pi*Ra/x)+Rb*np.exp(-pi*Rb/x))/x**2
#    return f


#Rs = op.newton(VdP, ((Ra+Rb)/2),fprime = VdP_1, args = (Ra, Rb), tol=(10^-10), maxiter = 5000)


a = set_up()

initialise(I,a)
G = gain(float(2),a)
print (meas_vdp(N,cont_Ra,a,G))

#def mob (t,gain,meas,R,avg,instr,Rs):
#    instr.write("ONI")
#    gain()
#    meas()
#    avg()
#    R()
#    Rhs=
#    Rh=
#    n=
#    return Rhs, Rh, n




#add in: resistance calculation, takes 1st array divides by second.
#Averaging and SD func that works for any array so we can have <V>, <I>, <R_test>, Ra and Rb
#set script so that we run the tests, do an average, print/check agreement
#then measure V and I DONE, calculate R and take average to give Ra
#then measure V and I DONE, calculate R and take average to give Rb
#define of our f(x) and f'(x) van der pauw relations using Ra and Rb where x is sheet resistance
#stick f(x) and f'(x) in scipy.optimise.newton(f(x),<Rab>, f'(x),args=(Ra,Rb),tol=0.0000000001,maxiter=5000)
  
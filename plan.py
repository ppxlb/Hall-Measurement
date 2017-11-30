# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

import numpy as np
from visa import ResourceManager

cont_test = np.array([12,23,34,41,13,24])
cont_Ra = np.array([[43,21],[34,21],[12,43],[21,43]])
cont_Rb = np.array([[23,41],[32,41],[41,32],[14,32]]) #Both of these require ADVANCED indexing
## OR
#cont_Ra = np.array([[43,34,12,21],[21,21,43,43]])
#cont_Rb = np.array([[23,32,41,14],[41,41,32,32]])
I = float(input("Current: "))
N = int(round(float(input("Sampling Count: "))))

def set_up():
    addr = ["GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"]
    rm = ResourceManager()
    instrs = []
    for x in range(0,3):
        instrs.append(rm.open_resource(addr[x], read_termination = "\n"))
    return instrs

def initialise(I,instrs):
    instrs[1].write('A') #set current mode to AC (set "D" for DC but redundant)
    instrs[0].write('SO') #not sure what this does to the instrument but it's needed
    curr = "I"+str(I) #create and stringify current message using out current argument
    instrs[1].write(curr) #send our desired current
    instrs[2].write('G0') #set gain G = 0
    instrs[2].write('H256') #set gain H = 256
    
def meas(N, cont, instrs):
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
#    arr_R = np.empty([len(cont),N]) #same for resistance
    for x in range(0,len(cont)):
        S = "S"+str(cont[x]) #make and stringify source contact probe setting
        M = "M"+str(cont[x]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[0].write(S) #set source contact probes
            instrs[0].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[2].read() #read volatage in to some variable, insert to our arrays
            arr_I[(x,y)] = instrs[1].read() #read current in to some variable
    return arr_V, arr_I

a = set_up()

initialise(I,a)
print(meas(N,cont_test,a))
    
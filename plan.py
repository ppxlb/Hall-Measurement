# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

import numpy as np
from visa import ResourceManager

#Define presets that never change
addr = np.array(["GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"])
cont_test = np.array([12,23,34,41,13,24])
cont_Ra = np.array([[43,21],[34,21],[12,43],[21,43]])
cont_Rb = np.array([[23,41],[32,41],[41,32],[14,32]]) #Both of these require ADVANCED indexing
## OR
#cont_Ra = np.array([[43,34,12,21],[21,21,43,43]])
#cont_Rb = np.array([[23,32,41,14],[41,41,32,32]])
I = float(input("Current: "))
N = float(input("Sampling Count: "))

def set_up(I,addr):
    rm = ResourceManager()
     #open the current address on instrument (all termination characters are \n)
    instr3_8 = rm.open_resource(addr[1], read_termination = "\n")
    instr3_8.write('A') #set current mode to AC (set "D" for DC but redundant)
    #open the setup address on instrument
    instr3_7 = rm.open_resource(addr[0], read_termination = "\n")
    instr3_7.write('SO') #not sure what this does to the instrument but it's needed
    curr = "I"+I #create and stringify current message using out current argument
    instr3_8.write(curr) #send our desired current
    #open the voltage address on instrument
    instr3_9 = rm.open_resource(addr[2], read_termination = "\n")
    instr3_9.write('G0') #set gain G = 0
    instr3_9.write('H256') #set gain H = 256
    
def Meas(N, cont):
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
#    arr_R = np.empty([len(cont),N]) #same for resistance
    for x in range(0,len(cont)):
        S = "S"+str(cont[x]) #make and stringify source contact probe setting
        M = "M"+str(cont[x]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instr3_7.write(S) #set source contact probes
            instr3_7.write(M) #set measurement contact probes
            Vin = instr3_9.read() #read volatage in to some variable
            Iin = instr3_8.read() #read current in to some variable
            arr_V[(x,y)] = Vin #insert to our arrays
            arr_I[(x,y)] = Iin
    return arr_V, arr_I        
    
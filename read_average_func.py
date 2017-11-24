# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 12:11:23 2017

@author: ppxlb
"""
import numpy as np
from visa import ResourceManager

def Ia(): #function to ask the user for the desired current
    I = "I" + input('current: ')
    return I

def rpts(): #function to ask the user for the desired number of repetitions to average over
    R = int(round(float(input('No. of repeats? '))))
    return R

def read_R(I,rp=2): #func to READ and calculate resistances between each probe permutation
    #setup, current and voltage respective ADDResses on instrument
    addr = np.array(["GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"])
    cont = np.array([12,23,34,41,13,24]) # CONTact probe permutations
    rm = ResourceManager() #shorthand access pyvisa to handle instrument
    i = 0 #create iteration count variables
    rp1 = rp + 1
    arr_V = np.empty([6,rp1]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([6,rp1]) #same for current
    arr_R = np.empty([6,rp1]) #same for resistance
    #arr_R[0-6] can be determined from cont variable
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
    while i < 6: #loop to measure over each
        j = 0 #reset to 0
        src = "S"+str(cont[i]) #make and stringify source contact probe setting
        meas = "M"+str(cont[i]) #make and stringify measurement contact probe setting
        while j <= rp:
            instr3_7.write(src) #set source contact probes
            instr3_7.write(meas) #set measurement contact probes
            Vin = instr3_9.read() #read volatage in to some variable
            Iin = instr3_8.read() #read current in to some variable
            arr_V[(i,j)] = Vin #insert to our arrays
            arr_I[(i,j)] = Iin
            j += 1 #add to our iteration count
        i += 1
    np.divide(arr_V,arr_I,arr_R) #R=V/I
    return {'R':arr_R,'I':I,'N':rp1} #spit out our resistance, current and no. of measurements

def R_stats (arr_R,N):
    cont_av = np.empty(6)#individual contacts average
    cont_sd = np.empty(6)#standard deviations for 6 contact averages
    for i in range(0,6):
        cont_av[i]=np.mean(arr_R[i])
        cont_sd[i]=np.std(arr_R[i])
    tot_av = np.mean(cont_av)#overall average
    tot_sd = np.mean(cont_sd)#overall standard deviation
    return cont_av,cont_sd, tot_av,tot_sd

a = read_R(Ia(),rpts())

print(a)
print()
print(R_stats(a["R"],a["N"]))
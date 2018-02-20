# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:36 2018

@author: ppxlb
"""
import numpy as np

def meas(N, cont, instrs, G):
    """
    ---------------------------------------------------------------------------
    
    Primary measure N times (float) function to be called to read from 
    contacts defined in an array in cont, using the instrs first assigned as an 
    array in set_up() and then primed in initialise(). The gain can be set 
    using gain() or a default 0 gain would be G = 0 H = 255.
    
    Used principally for check contacts operation.
    
    Gains are resent with each measurement for peace of mind it's fixed across 
    the repeats.
    
    Outputs a np array of voltage values and a seperate array of current values.
    
    ---------------------------------------------------------------------------
    """
    arr_V = np.empty([len(cont),N]) #empty arrays for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
    for x in range(0,len(cont)):
        S = "S"+str(cont[x]) #make and stringify source contact probe setting
        M = "M"+str(cont[x]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            instrs[3].write("G"+str(G[0]))
            instrs[3].write("H"+str(G[1]))
            arr_V[(x,y)] = instrs[3].read() #read volatage in to some variable, insert to our arrays
            arr_I[(x,y)] = instrs[2].read() #read current in to some variable
    return arr_V, arr_I

def meas_vdp(N, cont, instrs, G):
    """
    ---------------------------------------------------------------------------
    
    Very similar to meas() but takes in a different form of contacts cont array
    of 2D shape.
    
    Measure N times (float) function to be called to read from 
    contacts defined in an array in cont, using the instrs first assigned as an 
    array in set_up() and then primed in initialise(). The gain can be set 
    using gain() or a default 0 gain would be G = 0 H = 255.
    
    Used for sheet resistivity and hall measurements.
    
    Gains are resent with each measurement for peace of mind it's fixed across 
    the repeats.
    
    Outputs a np array of voltage values and a seperate array of current values.
    
    ---------------------------------------------------------------------------
    """
    arr_V = np.empty([len(cont), N]) #empty arrays of length 6*N for collecting voltage
    arr_I = np.empty([len(cont), N]) #same for current
    for x in range(0, len(cont)):
        S = "S"+str(cont[x,0]) #make and stringify source contact probe setting
        M = "M"+str(cont[x,1]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[3].write("G"+str(G[0]))
            instrs[3].write("H"+str(G[1]))
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[3].read() #read voltage, insert to our arrays
            arr_I[(x,y)] = instrs[2].read() #read current,
    return arr_V, arr_I
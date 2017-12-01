# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:54:58 2017

@author: ppxlb
"""
import numpy as np
cont_Ra = np.array([[43,21],[34,12],[12,34],[21,43]])
cont_Rb = np.array([[23,41],[32,14],[41,23],[14,32]]) #Both of these require ADVANCED indexing
cont_test = np.array([[12],[23],[34],[41],[13],[24]])

print(cont_test[1,0])

def meas(N, cont, instrs):
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
#    arr_R = np.empty([len(cont),N]) #same for resistance
    for x in range(0,len(cont)):
        S = "S"+str(cont[x,1]) #make and stringify source contact probe setting
        M = "M"+str(cont[x,0]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[0].write(S) #set source contact probes
            instrs[0].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[2].read() #read volatage in to some variable, insert to our arrays
            arr_I[(x,y)] = instrs[1].read() #read current in to some variable
    return arr_V, arr_I

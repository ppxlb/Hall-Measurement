# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:38 2018

@author: ppxlb
"""

import numpy as np

def avg (arr, N):
    """
    ---------------------------------------------------------------------------
    
    Averaging for read values takes in an array of V, I or R of length N.
    
    For multiple measurements N, each one will be averaged individually i.e.
    there will be a list of the average value for each configuration of pins 
    read.
    
    Returns 2 lists of floats the mean and standard deviation.
    
    ---------------------------------------------------------------------------
    """    
    av=np.empty(len(arr),dtype=float)
    sd=np.empty(len(arr),dtype=float)
    for i in range (0,len(arr)):
        av[i] = np.mean(arr[i])
        sd[i] = np.std(arr[i])
    return av, sd


def R (V, I, V_sd, I_sd):
    """
    ---------------------------------------------------------------------------
    
    A simple ohmic resistance calculation useful for both resistivity and hall 
    measurements. Put in the averaged V and I lists and the quotient will be 
    taken, accounting for conversion from uA to A. An equivalent operation is 
    performed on the standard deviation, however there are issues with the 
    quotient tending to infinity so in most cases the SD between resistances is
    adequate.
    
    The 4 values returned are a the mean resistance over all measurements Rav and 
    associated SD SDf, a list of resistances for each (already averaged) 
    measurement taken R.
    
    ---------------------------------------------------------------------------
    """  
    R = V/(I/1000000)
    Rav = np.mean(R)
    SDf = np.std(R)
    return Rav,SDf,R
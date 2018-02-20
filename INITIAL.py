# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:30 2018

@author: ppxlb
"""


def initialise(instrs,I = 100):
    """
    ---------------------------------------------------------------------------
    
    This function sends the first messages the instrument always needs before 
    a measurement can be done.
    
    Args are current I (float) in um input by user 
    usually ~100um and instrument addesses (np array) instrs from set_up().
    
    Should only be needed once but can be recalled to reset initial conditions 
    should pyvisa or instrument fail etc.
    
    ---------------------------------------------------------------------------
    """
    instrs[2].write('A') #set current mode to AC (set "D" for DC but redundant)
    instrs[1].write('SO') #not sure what this does to the instrument but it's needed
    curr = "I"+str(I) #create and stringify current message using out current argument
    instrs[2].write(curr) #send our desired current
    instrs[3].write('G0') #set gain G = 0
    instrs[3].write('H255') #set gain H = 255
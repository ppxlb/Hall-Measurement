# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:27 2018

@author: ppxlb
"""
from pyvisa import ResourceManager

def set_up():
    """
    ---------------------------------------------------------------------------
    
    Assigns the addresses to an object, calls the pyvisa class that controls
    instrument functions and assigns the \n read termination necessary.
    
    Can be re called the reassign variables or reiterate read termination in 
    event of pyvisa failure etc.
    
    ---------------------------------------------------------------------------
    """
    addr = ["GPIB0::3::0::INSTR","GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"] #create list of address name strings
    rm = ResourceManager() #open pyvisa class for control and assign to rm
    instrs = [] #create empty list to store address instances
    for x in range(0,4): #do 4 times
        instrs.append(rm.open_resource(addr[x], read_termination = "\n")) #make each address a resource manager instance and assign the relevant read termination "\n"
    return instrs #return our list of instances
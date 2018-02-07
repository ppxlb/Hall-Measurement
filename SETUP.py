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
    addr = ["GPIB0::3::0::INSTR","GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"]
    rm = ResourceManager()
    instrs = []
    for x in range(0,4):
        instrs.append(rm.open_resource(addr[x], read_termination = "\n"))
    return instrs
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:47:18 2017

@author: ppxlb
"""
import numpy as np
import visa

def curr_main():
    I = "I" + input('current: ')
    return I


def rpts():
    R = int(round(float(input('No. of repeats? '))))
    return (R)
    
    



def read_av (I):
    addr = np.array(["GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"])
    cont = np.array([12,23,34,41,13,24])
    rm = visa.ResourceManager()
    i = 0
    arr_V = np.array([])
    arr_I = np.array([])
    while i < 6:
        instr3_8 = rm.open_resource(addr[1], read_termination = "\n")
        instr3_8.write('A')
        instr3_7 = rm.open_resource(addr[0], read_termination = "\n")
        instr3_7.write('SO')
        curr = "I"+I
        instr3_8.write(curr)
        instr3_9 = rm.open_resource(addr[2], read_termination = "\n")
        instr3_9.write('G0') #gain G = 0
        instr3_9.write('H256') #gain H = 256
        src = "S"+cont[i]
        instr3_7.write(src)
        meas = "M"+cont[i]
        instr3_7.write(meas)
        i += 1
        arr_V += instr3_9.read()
        arr_I += instr3_8.read()
        return arr_V,arr_I
    print (arr_I, arr_V)
    arr_R = arr_V/arr_I
    return arr_R

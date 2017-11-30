# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:17:09 2017

@author: localadmin
"""
from visa import ResourceManager
def set_up():
    addr = ["GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"]
    rm = ResourceManager()
    instrs = []
    for x in range(0,3):
        instrs.append(rm.open_resource(addr[x], read_termination = "\n"))
    return instrs
#instr = set_up()
#print(instr[0])
###rote alternative
#def set_up():
#    addr = np.array(["GPIB0::3::0::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"])
#    rm = ResourceManager()
#    instr3_7 = rm.open_resource(addr[0], read_termination = "\n")
#    instr3_8 = rm.open_resource(addr[1], read_termination = "\n")
#    instr3_9 = rm.open_resource(addr[2], read_termination = "\n")
#    return instr3_7,instr3_8,instr3_9
#
#instr = set_up()
#
#print(instr[0].read())
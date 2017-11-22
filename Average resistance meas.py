# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import visa
rm = visa.ResourceManager()
instr3_8 = rm.open_resource('GPIB0::3::8::INSTR', read_termination = "\n")
print(instr3_8.write('A'))
instr3_7 = rm.open_resource('GPIB0::3::7::INSTR', read_termination = "\n")
instr3_7.write('SO')
instr3_8.write('I100')
instr3_9 = rm.open_resource('GPIB0::3::9::INSTR', read_termination = "\n")
instr3_9.write('G0') #gain G = 0
instr3_9.write('H256') #gain H = 256
instr3_7.write('S13')
instr3_7.write('M13')
print(instr3_9.read(),instr3_8.read()) #Print Voltage reading, Current reading








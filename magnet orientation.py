# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:43:49 2017

@author: localadmin
"""

import visa
rm = visa.ResourceManager()
instr = rm.open_resource('GPIB0::3::0::INSTR')
instr.read_termination = '\n'
print(instr.write("ON"))

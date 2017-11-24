# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:27:53 2017

@author: ppxlb
"""

from inputs import Ia, rpts
from resistance import read_R
from averages import R_stats

a = read_R(Ia(),rpts())#measure resistances with user input values

print(a)
print()
print(R_stats(a["R"],a["N"])) #find the average(s) and standard deviation(s)
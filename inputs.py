# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:17:43 2017

@author: ppxlb
"""

def Ia(): #function to ask the user for the desired current
    I = "I" + input('current: ')
    return I

def rpts(): #function to ask the user for the desired number of repetitions to average over
    R = int(round(float(input('No. of repeats? '))))
    return R
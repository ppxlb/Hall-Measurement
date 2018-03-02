# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:44:14 2018

@author: ppxlb
"""

import numpy as np

def chck(meas, avg, instrs, dline, Txt, tk):
    cont_test = np.array([12,23,34,41,13,24])
    tests = meas(1, cont_test, instrs, (0,255))
    results = avg(tests[0])
    x=0
    Txt.insert(tk.END,dline+"\n"+"Contacts read:"+"\n")
    for i in results[0]:
        Txt.insert(tk.END,(str(cont_test[x])[0]+" to "+(str(cont_test[x])[1]+" = "+str(i)+" V\n")))
        x=x+1
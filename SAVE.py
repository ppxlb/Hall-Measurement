# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:06:01 2018

@author: localadmin
"""
import datetime as DT

def Save(samp_nam,Txt,tk):
    TxtValue=Txt.get("1.0","end-1c")
    f = open("Hall_"+str(samp_nam)+".txt",'w')
    f.write(str(samp_nam))
    f.write("\n")
    f.write(str(DT.datetime.now()))
    f.write("\n")
    f.write(str(TxtValue))
    f.close
    
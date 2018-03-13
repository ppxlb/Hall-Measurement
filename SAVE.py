# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 12:06:01 2018

@author: localadmin
"""
import datetime as DT #date and time module for record keeping 
import os.path #module to write to a specific path

def save(samp_nam,I,t,dline,Txt,tk):
    """
    Simple save function that reads whatever is on the text box and sends to a 
    .txt file with the name given from the sample name, saved in a specific
    folder in documents.
    """
    TxtValue=Txt.get("1.0","end-1c") #get all text from resutls text box
    f = open(os.path.join('C:\\Users\\localadmin\\Documents\\Hall Measurements', "Hall_"+str(samp_nam)+".txt"),'a+') #open file with relevant sample name creating one if not already there
    f.write(str(samp_nam)) #put sample name at top
    f.write("\n") #new line 
    f.write(str(DT.datetime.now())) #add date and time for record keeping
    f.write("\n")
    f.write("Current: "+str(I)+" uA") #add current used
    f.write("\n")
    f.write("Sample Thickness: "+str(t)+" um") #add given thickness 
    f.write("\n")
    f.write(dline) #generic line break    
    f.write("\n")
    f.write(str(TxtValue)) #write everything on the tXt box
    f.close #close file
    
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:45:31 2018

@author: ppxlb
"""
import numpy as np
from time import sleep

def bulk(t,Txt,tk):
    f = open('temp.txt','r')
    SCC = float(f.readlines()[1].strip())
    f.close()
    HSC = (1/(SCC*(1.602*10**-19)))
    CC = SCC/(t*0.0001)
#    CC_err = CC*np.sqrt(((SCC_err/SCC)**2)+((t_err/t)**2))
    Txt.insert(tk.END,"Carrier Concentration: "+str("%.3g" % CC)+" "+"cm^-3"+"\n")
    HC = HSC*t*0.0001
#    HC_err = HC*np.sqrt(((HSC_err/HSC)**2)+((t_err/t)**2))
    Txt.insert(tk.END,"Hall Coefficient: "+str("%.3g" % HC)+" "+"cm^-3/C"+"\n")

def hall (instr, gain, meas, avg, R, N, dline, t, Txt, tk, I = 100, Vt = 2):
    """
    ---------------------------------------------------------------------------
    This is the Hall measurement function and by far the most complex it 
    includes setting up the instrument, controlling the magnet, taking readings 
    and doing a host of caluclations to give numerous results.
    
    There are multiple arguments that are needed for functions that are 
    themselves arguments:
        instr: from set_up() this is an array addresses for the GPIB that will 
        be used in measurements and gain calculations.
        
        gain: this function is read in to recalculate the gain for the contact 
        configuration of a hall measurement witht he magnet inplace over the 
        sample.
        
        meas: this function is taken as an argument so that measurements can be 
        done with out specific hall contact configuration with the magnet in 
        place.
        
        avg: averaging and standard deviation function to find the average of N 
        measured values for each configuration both V and I.
        
        R: a function for taking the quotient of V and I for an ohmic 
        resistance value.
        
        N: the number of measurement repeats to be made (int)
        
        I: user input cuurent in uA (float)
        
        Vt: the gain target voltage, historically 2V but up to 4V (float)
        
        t: given thickness of sample for carrier concentration and hall 
        coefficient
        
        Txt: results text box instance for displaying values
        
        tk: GUI instance for textbox keywords
        
        dline: generic line break string
        
    The process of the function begins by defining our contact configuration. 
    The magnet is then instructed to orientate north whilst out from the stage 
    then move into the sample stage, 12 seconds is left for this, an error at 
    this stage may suggest the magnet needs to be moved manually.
    
    A gain adjustment is taken with the magnet in place using 0 and 255 and 
    initial gain estimates. 
    The first measurement is taken with the magnet is the north orientation as 
    VIn, averages are found of each measurement in V and I and the V values 
    have the gain fudging reversed to give the actual voltage. The magnet is 
    then sent back out from the stage to rotate to the south orientation with a 
    12 second window.
    
    The second measurement is then taken as VIs and the same averaging steps 
    follow. The magnet is sent back out for good and calculation of results to 
    be returned begins.
    
    First the Hall voltage VH is found as the difference between north 
    and south voltages. The Hall resistance RH and error is calculated in a 
    similar fashion and used for all the succeeding results. They are the Sheet 
    Carrier Concentration SCC the number of charge carriers in a 1cm by 1cm 
    square of our sample, mobility 'mob' using the Rs from the resistivity 
    measurement saved to the temp file and the Hall sheet coefficient HSC. The 
    SCC is then written to the temp file amd the Charge Carrier Concentration 
    CC, which is a 3D measure of charge carrier density and Hall coefficient HC
    measures of ratio of electric field to magnetic field by current density 
    are calculated in another fucntion.
    
    All these values are printed in standard form to 3 sig fig to the GUI text 
    box. 
    
    error calculations are commented out as unneccesary.
    ---------------------------------------------------------------------------
    """
    cont_h = np.array([[31,42],[13,24],[42,13],[24,31]])
    instr[2].write("I"+str(I)) #send our desired current
    G = gain(Vt, instr)
    GH = gain(Vt, instr, G, cont = (13,42))
    instr[0].write("ONI")
    sleep(12)
    VIn = meas(N, cont_h, instr, GH)
    Vn = avg((VIn[0]/((255/GH[1])*10**GH[0])))
    In = avg(VIn[1])
    instr[0].write("OSI")
    sleep(16)
    VIs = meas(N, cont_h, instr, GH)
    Vs = avg((VIs[0]/((255/GH[1])*10**GH[0])))
    Is = avg(VIs[1])
    instr[0].write("ON")
    VH = (sum(Vn[0]-Vs[0]))/8
#    VH_err = (sum(Vn[1]+Vs[1]))/(8*(N**0.5))
    Txt.insert(tk.END,dline+"\n"+"Overall Hall Voltage: "+str("%.3g" % VH)+" "+"V"+"\n")
    Rn = R(Vn[0],In[0],Vn[1],In[1])
    Rs = R(Vs[0],Is[0],Vs[1],Is[1])
    RH = (sum(Rn[2])-sum(Rs[2]))/8
#    RH_err = (Rn[1]+Rs[1])/(8*(N**0.5))
    Txt.insert(tk.END,"Hall Resistance: "+str(round(RH,1))+" "+"Ohm"+"\n")
    SCC = (0.288*10**-4)/((-1.602*10**-19)*RH)
#    SCC_err = SCC*RH/RH_err
    Txt.insert(tk.END,"Sheet Carrier Concentration: "+str("%.3g" % SCC)+" "+"cm^-2"+"\n")
    HSC = (1/(SCC*(1.602*10**-19)))
#    HSC_err = HSC*SCC/SCC_err
    Txt.insert(tk.END,"Hall Sheet Coefficient: "+str("%.3g" % HSC)+" "+"cm^-2/C"+"\n")
    f = open('temp.txt','r')
    Rs = float(f.readlines()[0].strip())
    f.close()
    f = open('temp.txt','a')
    f.write("\n"+str(SCC))
    f.close()
    bulk(t,Txt,tk)
    mob = 1/((SCC*Rs)*(1.602*10**-19))
    Txt.insert(tk.END,"Hall Mobility: "+str("%.3g" % mob)+"cm^2/Vs"+"\n")
    #mob_err = mob*(np.sqrt(((Rs_err/Rs)**2)+(RH_err/h[2])))
    #print ("Hall Mobility: ", "%e" % mob, chr(177), "cm^2/Vs") #"%.g" % mob_err,
#    return VH, RH, SCC, CC, HSC, HC, VH_err, RH_err, SCC_err,CC_err, HSC_err,HC_err
    
def rebulk(bulk,t,dline,Txt,tk):
    Txt.insert(tk.END,dline+"\n"+"Given new thickness of "+str(t)+"um"+"\n")
    bulk(t,Txt,tk)
    
# +/- symbol is chr(177)
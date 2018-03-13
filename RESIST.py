# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:44:13 2018

@author: ppxlb
"""
import numpy as np
from scipy import optimize as op



def VdP (x, Ra, Rb):
    """
    ---------------------------------------------------------------------------
    
    The Van der Pauw equation that is iteratated over in the sheet resistivity 
    calculation later done via newton rhaphson.
    
    Rs values of increasing accuracy are input as x with the initial guess 
    being the mean of Ra and Rb. 
    
    An Rs candidate goes in and f(Rs) is returned, if it isn't sufficiently 
    close to 0 then another Rs is tried.
    
    ---------------------------------------------------------------------------
    """  
    pi = -np.pi
    f = np.exp(pi*Ra/x)+np.exp(pi*Rb/x)-1
    return f

def VdP_1 (x, Ra, Rb):
    """
    ---------------------------------------------------------------------------
    
    The 1st order differentiation of the Van der Pauw equation. This is also 
    iteratated over in the sheet resistivity calculation later done via newton rhaphson.
    
    It is needed to give the gradient at the point of x for the Newton rhapson 
    calculation.
    
    ---------------------------------------------------------------------------
    """ 
    pi = np.pi
    f = pi*(Ra*np.exp(-pi*Ra/x)+Rb*np.exp(-pi*Rb/x))/x**2
    return f

def ivity(t,Txt,tk):
    """
    -ivity as in we know sheet resistance Rs from 'resist' and this gives 
    resist'ivity' Rho using the former's Rs.
    All that's needed as arguments is the input thickness and the GUI instances
    to write to the text box. The Rs comes from a temp file that's wiped by 
    'resist()'. This is due to tkinter being fussy about needing lambda 
    functions to control buttons making returning values tricky.
    """
    Rs = float(open('temp.txt','r').readlines()[0].strip()) #read first line with no trailing end
    Rho = Rs*t*0.0001 #calculate resistivity
#    Rho_err = float(Rho*np.sqrt(((Rs_err/Rs)**2)+((t_err/t)**2)))
    Txt.insert(tk.END, "Resistivity: "+str("%.3g" % Rho)+" "+"Ohm.cm"+"\n")

def resist(instr, meas, avg, gain, R, N, dline, t, Txt, tk, I = 100, res = ivity):
    """
    Our main resistance measurement gives sheet resistance and calls for the 
    resistivity with 'ivity()' using a temp file to parse Rs.
    
    The contact configurations here are unique to each measurement to perform a 
    Van der Pauw reading. I is sent to the hall system, the appropriate gain 
    found and measurements of the a and b configuration found. From the 
    measurements the ohmic resistance is found and Ra and Rb are the points 
    required to run a newton rhaphson van der pauw calculation of Rs.
    
    Rs is sent to the GUI text box
    
    a temp file is then created/cleared and the Rs is written to be parsed to 
    the resistivity function which in turn produces a result.
    """
    cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]]) #first measurement contact config
    cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]]) #second measurement contact config (opposite)
    instr[2].write("I"+str(I)) #send our desired current
    G = gain(float(2),instr) #run a gain calculation aiming for 2V
    VIa = meas(N,cont_Ra,instr,G) #measure out first configuration N times
    Va = avg((VIa[0]/((255/G[1])*10**G[0]))) #average the voltages read
    Ia = avg(VIa[1]) #average the currents read
    Ra = R(Va[0],Ia[0],Va[1],Ia[1]) #calculate ohmic resistance
    VIb = meas(N,cont_Rb,instr,G) #measure the opposite configuration of probes
    Vb = avg((VIb[0]/((255/G[1])*10**G[0]))) #average these read voltages
    Ib = avg(VIb[1]) #average the current read
    Rb = R(Vb[0],Ib[0],Vb[1],Ib[1]) #find ohmic resistance
    x0 = (Ra[0]+Rb[0])/2 #take the midpoint of the two resistances as an initial guess of Rs
    if Ra[1] > Rb[1]: #IF statement for the certainty in our newton rhaphson
        Rs_err = (-(np.pi)*Ra[1]/(-0.69315))/(N**0.5)
    else:
        Rs_err = (-(np.pi)*Rb[1]/(-0.69315))/(N**0.5)
    Rs = float(op.newton(VdP, x0, fprime = VdP_1, args = (Ra[0], Rb[0]), maxiter = 1000))
    Txt.insert(tk.END, dline+"\n"+"Sheet Resistivity: "+str("%.3g" % Rs)+" "+chr(177)+" "+str("%.1g" % Rs_err)+" "+"Ohm/sq"+"\n")
    f = open('temp.txt','w')
    f.write(str(Rs))
    f.close()
    ivity(t,Txt,tk)
#    Rho = Rs*t*0.0001
#    Rho_err = float(Rho*np.sqrt(((Rs_err/Rs)**2)+((t_err/t)**2)))
#    print("Sheet Resistivity: ", "%e" % round(Rs,-1), chr(177),"%.e" % Rs_err, "Ohm/sq")
#    print("Resistivity: ", round(Rho,3),chr(177),"%.e" % Rho_err, "Ohm.cm")    
#    Txt.insert(tk.END, "Resistivity: "+str(round(Rho,3))+" "+chr(177)+" "+str(round(Rho_err,1))+" "+"Ohm.cm"+"\n")
#    return Rs, Rho, Ra, Rb, Rs_err, Rho_err

def reivity(ivity,t,dline,Txt,tk):
    """
    a short funciton to rerun ivity with a new t.
    """
    Txt.insert(tk.END,dline+"\n"+"Given new thickness of "+str(t)+"um"+"\n")
    ivity(t,Txt,tk)
    


#set script so that we run the tests, do an average, print/check agreement
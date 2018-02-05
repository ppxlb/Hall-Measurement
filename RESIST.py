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

def resistivity(instr, gain, meas_vdp, avg, R, N, Ga, dline, t, t_err, Txt, tk):
    cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
    cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]])
    VIa = meas_vdp(N,cont_Ra,instr,Ga)
    Va = avg((VIa[0]/((255/Ga[1])*10**Ga[0])),N)
    Ia = avg(VIa[1],N)
    Ra = R(Va[0],Ia[0],Va[1],Ia[1])

    VIb = meas_vdp(N,cont_Rb,instr,Ga)
    Vb = avg((VIb[0]/((255/Ga[1])*10**Ga[0])),N)
    Ib = avg(VIb[1],N)
    Rb = R(Vb[0],Ia[0],Va[1],Ia[1])

    x0 = (Ra[0]+Rb[0])/2

    if Ra[1] > Rb[1]:
        Rs_err = (-(np.pi)*Ra[1]/(-0.69315))/(N**0.5)
    else:
        Rs_err = (-(np.pi)*Rb[1]/(-0.69315))/(N**0.5)

    Rs = float(op.newton(VdP, x0, fprime = VdP_1, args = (Ra[0], Rb[0]), maxiter = 5000))
    Txt.insert(tk.END, dline+"\n"+"Sheet Resistivity: "+str("%e" % round(Rs,-1))+" "+chr(177)+" "+str("%.e" % Rs_err)+" "+"Ohm/sq"+"\n")
    Rho = Rs*t*0.0001
    Rho_err = float(Rho*np.sqrt(((Rs_err/Rs)**2)+((t_err/t)**2)))
#    print("Sheet Resistivity: ", "%e" % round(Rs,-1), chr(177),"%.e" % Rs_err, "Ohm/sq")
#    print("Resistivity: ", round(Rho,3),chr(177),"%.e" % Rho_err, "Ohm.cm")    
    Txt.insert(tk.END, "Resistivity: "+str(round(Rho,3))+" "+chr(177)+" "+str(round(Rho_err,1))+" "+"Ohm.cm"+"\n")
    return Rs, Rho, Ra, Rb, Rs_err, Rho_err
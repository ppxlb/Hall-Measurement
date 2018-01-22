# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

import numpy as np
from visa import ResourceManager
from scipy import optimize as op
from time import sleep
import tkinter as tk


### GUI set up ###
#window = tk.Tk()
#scrollbar = tk.Scrollbar(window)
#scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70)
#Txt.pack(side=tk.RIGHT)
#test_btn = tk.Button(window, text = "Check contacts", command = chck)
#test_btn.pack(side=tk.LEFT)
#window.title("HALL 9000")
#window.geometry("1200x800")
#window.wm_iconbitmap("HALL9000.ico")
#window.mainloop()


cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]]) #Both of these require ADVANCED indexing
cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])



I = float(input("Current (uA): "))
N = int(round(float(input("Sampling Count: "))))
t = float(input("thickness (um): "))
t_err = float(input("thickness error (um): "))
def set_up():
    """
    ---------------------------------------------------------------------------
    
    Assigns the addresses to an object, calls the pyvisa class that controls
    instrument functions and assigns the \n read termination necessary.
    
    Can be re called the reassign variables or reiterate read termination in 
    event of pyvisa failure etc.
    
    ---------------------------------------------------------------------------
    """
    addr = ["GPIB0::3::0::INSTR","GPIB0::3::7::INSTR","GPIB0::3::8::INSTR","GPIB0::3::9::INSTR"]
    rm = ResourceManager()
    instrs = []
    for x in range(0,4):
        instrs.append(rm.open_resource(addr[x], read_termination = "\n"))
    return instrs

def initialise(I,instrs):
    """
    ---------------------------------------------------------------------------
    
    This function sends the first messages the instrument always needs before 
    a measurement can be done.
    
    Args are current I (float) in um input by user 
    usually ~100um and instrument addesses (np array) instrs from set_up().
    
    Should only be needed once but can be recalled to reset initial conditions 
    should pyvisa or instrument fail etc.
    
    ---------------------------------------------------------------------------
    """
    instrs[2].write('A') #set current mode to AC (set "D" for DC but redundant)
    instrs[1].write('SO') #not sure what this does to the instrument but it's needed
    curr = "I"+str(I) #create and stringify current message using out current argument
    instrs[2].write(curr) #send our desired current
    instrs[3].write('G0') #set gain G = 0
    instrs[3].write('H255') #set gain H = 255
    
def meas(N, cont, instrs, G):
    """
    ---------------------------------------------------------------------------
    
    Primary measure N times (float) function to be called to read from 
    contacts defined in an array in cont, using the instrs first assigned as an 
    array in set_up() and then primed in initialise(). The gain can be set 
    using gain() or a default 0 gain would be G = 0 H = 255.
    
    Used principally for check contacts operation.
    
    Gains are resent with each measurement for peace of mind it's fixed across 
    the repeats.
    
    Outputs a np array of voltage values and a seperate array of current values.
    
    ---------------------------------------------------------------------------
    """
    arr_V = np.empty([len(cont),N]) #empty arrays for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
    for x in range(0,len(cont)):
        S = "S"+str(cont[x]) #make and stringify source contact probe setting
        M = "M"+str(cont[x]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            instrs[3].write("G"+str(G[0]))
            instrs[3].write("H"+str(G[1]))
            arr_V[(x,y)] = instrs[3].read() #read volatage in to some variable, insert to our arrays
            arr_I[(x,y)] = instrs[2].read() #read current in to some variable
    return arr_V, arr_I

def gain(Vt, instrs, G = (0,255), cont = (12,43)):
    """
    ---------------------------------------------------------------------------
    
    This function tests and then adjusts the voltage gain G (logarithm) and H
    (multiple). It works towards a target voltage, historically 2V but 
    feasilbly up to 4V.
    
    The target Vt can be set by the user as a float or int 0<Vt<4. Instruments 
    are assigned in set_up() as instrs whilst initial gain is taken as a list 
    or array of 2 values G the exponent and H the multiplier. Contacts can be 
    set as either a check (12,12), sheet (12,43) or hall measurement (13,42).
    
    It takes the ratio of the target to gain-boosted read voltage and then 
    changes it appropriately. Repeated measurements will cycle the exponent 
    gain and the ratio nears 1 it seems to upset the decision statements.
    
    A list is returned with the new exponent and multiplier (G,H) but this 
    isn't applied automatically.
    ---------------------------------------------------------------------------
    """
    instrs[3].write("G"+str(G[0])) #set gain G
    instrs[3].write("H"+str(G[1])) #set gain H
    instrs[1].write("S"+str(cont[0])) #set source contact probes
    instrs[1].write("M"+str(cont[1])) #set measurement contact probes
    u = abs(Vt/(float(instrs[3].read()))) #ratio of target voltage Vt to measured voltage 
    if u <= 10:
        return 0, 255/u #u UNSURE THIS WORKS maybe {G=1, 255/u} works or {G=0, H = 25.5*u}
    elif u> 10 and u < 100:
        return 1, 2550/u
    elif u >= 100 and u < 1000:
        return 2, 25500/u
    elif u >= 1000 and u < 255000:
        return 3, 255000/u
    else:
        print ("error in gain determination")

def meas_vdp(N, cont, instrs,G):
    """
    ---------------------------------------------------------------------------
    
    Very similar to meas() but takes in a different form of contacts cont array
    of 2D shape.
    
    Measure N times (float) function to be called to read from 
    contacts defined in an array in cont, using the instrs first assigned as an 
    array in set_up() and then primed in initialise(). The gain can be set 
    using gain() or a default 0 gain would be G = 0 H = 255.
    
    Used for sheet resistivity and hall measurements.
    
    Gains are resent with each measurement for peace of mind it's fixed across 
    the repeats.
    
    Outputs a np array of voltage values and a seperate array of current values.
    
    ---------------------------------------------------------------------------
    """
    arr_V = np.empty([len(cont),N]) #empty arrays of length 6 for collecting voltage
    arr_I = np.empty([len(cont),N]) #same for current
    for x in range(0,len(cont)):
        S = "S"+str(cont[x,0]) #make and stringify source contact probe setting
        M = "M"+str(cont[x,1]) #make and stringify measurement contact probe setting
        for y in range(0,N):
            instrs[3].write("G"+str(G[0]))
            instrs[3].write("H"+str(G[1]))
            instrs[1].write(S) #set source contact probes
            instrs[1].write(M) #set measurement contact probes
            arr_V[(x,y)] = instrs[3].read() #read voltage, insert to our arrays
            arr_I[(x,y)] = instrs[2].read() #read current,
    return arr_V, arr_I

def avg (arr, N):
    """
    ---------------------------------------------------------------------------
    
    Averaging for read values takes in an array of V, I or R of length N.
    
    For multiple measurements N, each one will be averaged individually i.e.
    there will be a list of the average value for each configuration of pins 
    read.
    
    Returns 2 lists of floats the mean and standard deviation.
    
    ---------------------------------------------------------------------------
    """    
    av=np.empty(len(arr),dtype=float)
    sd=np.empty(len(arr),dtype=float)
    for i in range (0,len(arr)):
        av[i] = np.mean(arr[i])
        sd[i] = np.std(arr[i])
    return av, sd
    
def R (V, I, V_sd, I_sd):
    """
    ---------------------------------------------------------------------------
    
    A simple ohmic resistance calculation useful for both resistivity and hall 
    measurements. Put in the averaged V and I lists and the quotient will be 
    taken, accounting for conversion from uA to A. An equivalent operation is 
    performed on the standard deviation, however there are issues with the 
    quotient tending to infinity so in most cases the SD between resistances is
    adequate.
    
    The 4 values returned are a the mean resistance over all measurements Rav and 
    associated SD SDf, a list of resistances for each (already averaged) 
    measurement taken R.
    
    ---------------------------------------------------------------------------
    """  
    R = V/(I/1000000)
    Rav = np.mean(R)
    SDf = np.std(R)
    return Rav,SDf,R

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

#def meas_VH(N, cont, instrs, G):
#    arr_V = np.empty([len(cont),N]) #empty arrays for collecting voltage
#    arr_I = np.empty([len(cont),N]) #same for current
#    for x in range(0,len(cont)):
#        S = "S"+str(cont[x,0]) #make and stringify source contact probe setting
#        M = "M"+str(cont[x,1]) #make and stringify measurement contact probe setting
#        for y in range(0,N):
#            instrs[1].write(S) #set source contact probes
#            instrs[1].write(M) #set measurement contact probes
#            instrs[3].write("G"+str(G[0]))
#            instrs[3].write("H"+str(G[1]))
#            arr_V[(x,y)] = instrs[3].read() #read volatage in to some variable, insert to our arrays
#            arr_I[(x,y)] = instrs[2].read() #read current in to some variable
#    return arr_V, arr_I

#def gainH(instrs, Vt = 2, G = 0, H = 255, cont = (13,42)):
#    instrs[3].write("G"+str(G)) #set gain G
#    instrs[3].write("H"+str(H)) #set gain H
#    instrs[1].write("S"+str(cont[0])) #set source contact probes
#    instrs[1].write("M"+str(cont[1])) #set measurement contact probes
#    u = abs(Vt/(float(instrs[3].read()))) #ratio of target voltage Vt to measured voltage 
#    if u <= 10:
#        return 0, 255/u #u UNSURE THIS DOESN'T WORK {G=1, 255/u} works or {G=0, H = 25.5*u}
#    elif u> 10 and u < 100:
#        return 1, 2550/u
#    elif u >= 100 and u < 1000:
#        return 2, 25500/u
#    elif u >= 1000 and u < 255000:
#        return 3, 255000/u
#    else:
#        print ("error in gain determination")

a = set_up()

initialise(I,a)
G = gain(float(2),a)
def chck(meas, avg, instrs):
    dline = "--------------------------------------------------"
    cont_test = np.array([12,23,34,41,13,24])
    tests = meas(1, cont_test, instrs, (0,255))
    results = avg(tests[0],N)
    x=0
    Txt.insert(tk.END,dline+"\n"+"Contacts read:"+"\n")
    for i in results[0]:
        Txt.insert(tk.END,(str(cont_test[x])[0]+" to "+(str(cont_test[x])[1]+" = "+str(i)+" V\n")))
        x=x+1

window = tk.Tk()
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70)
Txt.pack(side=tk.RIGHT)
test_btn = tk.Button(window, text = "Check contacts", command = lambda : chck(meas,avg,a) )
test_btn.pack(side=tk.LEFT)
window.title("HALL 9000")
window.geometry("1200x800")
window.wm_iconbitmap("HALL9000.ico")
window.mainloop()



def resistivity(instr, gain, meas, avg, R, N, Ga):
    cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
    cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]])
    VIa = meas_vdp(N,cont_Ra,a,Ga)
    Va = avg((VIa[0]/((255/Ga[1])*10**Ga[0])),N)
    Ia = avg(VIa[1],N)
    Ra = R(Va[0],Ia[0],Va[1],Ia[1])

    VIb = meas_vdp(N,cont_Rb,a,Ga)
    Vb = avg((VIb[0]/((255/Ga[1])*10**Ga[0])),N)
    Ib = avg(VIb[1],N)
    Rb = R(Vb[0],Ia[0],Va[1],Ia[1])

    x0 = (Ra[0]+Rb[0])/2

    if Ra[1] > Rb[1]:
        Rs_err = (-(np.pi)*Ra[1]/(-0.69315))/np.sqrt(N)
    else:
        Rs_err = (-(np.pi)*Rb[1]/(-0.69315))/np.sqrt(N)

    Rs = op.newton(VdP, x0, fprime = VdP_1, args = (Ra[0], Rb[0]), maxiter = 5000)
    Rho = Rs*t*0.0001
    Rho_err = Rho*np.sqrt(((Rs_err/Rs)**2)+((t_err/t)**2))
    print("Sheet Resistivity: ", "%e" % round(Rs,-1), chr(177),"%.e" % Rs_err, "Ohm/sq")
    print("Resistivity: ", round(Rho,3),chr(177),"%.e" % Rho_err, "Ohm.cm")
    return Rs, Rho, Ra, Rb, Rs_err, Rho_err

output2 = resistivity(a,gain,meas_vdp,avg,R,N,G)
#add in: resistance calculation, takes 1st array divides by second.
#Averaging and SD func that works for any array so we can have <V>, <I>, <R_test>, Ra and Rb
#set script so that we run the tests, do an average, print/check agreement

def Hall (instr, gain, meas, avg, R, N, I, Ga, Vt = 2):
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
    
    First the Hall voltage VH and error are found as the difference between north 
    and south voltages. The Hall resistance RH and error is calculated in a 
    similar fashion and used for all the succeeding results. They are the Sheet 
    Carrier Concentration SCC the number of char carriers in a 1cm by 1cm 
    square of our sample, the Charge Carrier Concentration CC, which is a 3D 
    measure of charge carrier density, the Hall sheet coefficient HSC and Hall 
    coefficient HC measures of ratio of electric field to magnetic field by 
    current density.
    
    All these values and their errors are printed in standard form and returned. 
    
    ---------------------------------------------------------------------------
    """
    cont_h = np.array([[31,42],[13,24],[42,13],[24,31]])
    instr[0].write("ONI")
    sleep(12)
    GH = gain(Vt, instr, Ga,  cont = (13,42))
#    print ("Gain values used: ", GH)
    VIn = meas_vdp(N, cont_h, a, GH)
    Vn = avg((VIn[0]/((255/GH[1])*10**GH[0])),N)
    In = avg(VIn[1],N)
    instr[0].write("OSI")
    sleep(12)
    VIs = meas_vdp(N, cont_h, a, GH)
    Vs = avg((VIs[0]/((255/GH[1])*10**GH[0])),N)
    Is = avg(VIs[1],N)
    instr[0].write("ON")
    VH = (sum(Vn[0]-Vs[0]))/8
    VH_err = (sum(Vn[1]+Vs[1]))/(8*np.sqrt(N))
    print ("Overall Hall Voltage: ", "%g" % VH,chr(177),"%.g" % VH_err, "V")
#    if VH < 0:
#        print ("Sample is N-type")
#    elif VH > 0:
#        print ("Sample is P-type")
    Rn = R(Vn[0],In[0],Vn[1],In[1])
    Rs = R(Vs[0],Is[0],Vs[1],Is[1])
    RH = (sum(Rn[2])-sum(Rs[2]))/8
    RH_err = (sum(Rn[1]+Rs[1]))/(8*np.sqrt(N))
    print ("Hall Resistance: ", round(RH,1), chr(177),"%.g" % RH_err, "Ohm")
    SCC = (0.288*10**-4)/((-1.602*10**-19)*RH)
    SCC_err = SCC*RH/RH_err
    print ("Sheet Carrier Concentration: ", "%e" % SCC,chr(177),"%.g" % SCC_err, "cm^-2")
    CC = SCC/(t*0.0001)
    CC_err = CC*np.sqrt(((SCC_err/SCC)**2)+((t_err/t)**2))
    print ("Carrier Concentration: ", "%e" % CC, chr(177),"%.g" % CC_err, "cm^-3")
    HSC = (1/(SCC*(1.602*10**-19)))
    HSC_err = HSC*SCC/SCC_err
    print ("Hall Sheet Coefficient: ", "%e" % HSC,chr(177),"%.g" % HSC_err, "cm^-2/C")
    HC = HSC*t*0.0001
    HC_err = HC*np.sqrt(((HSC_err/HSC)**2)+((t_err/t)**2))
    print ("Hall Coefficient: ", "%e" % HC,chr(177),"%.g" % HC_err, "cm^-3/C")
    return VH, RH, SCC, CC, HSC, HC, VH_err, RH_err, SCC_err,CC_err, HSC_err,HC_err

h = Hall(a, gain, meas_vdp, avg, R, N, I, G)
Rs = output2[0]
mob = 1/((h[2]*Rs)*(1.602*10**-19))
#mob_err = mob*(np.sqrt(((Rs_err/Rs)**2)+(RH_err/h[2])))
print ("Hall Mobility: ", "%e" % mob, chr(177), "cm^2/Vs") #"%.g" % mob_err,
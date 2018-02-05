# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:41:33 2018

@author: ppxlb
"""

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
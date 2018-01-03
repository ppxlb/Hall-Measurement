# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:21:51 2017

@author: ppxlb
"""

cont_mob = np.array([[31,42],[13,24],[42,13],[24,31]])
instr.write("ONI")
VIn = meas(N, cont_mob, a)
Vn = avg(VIn[0])
In = avg(VIn[1])
Rn = R(Vn[0],In[0],Vn[1],In[1])

instr.write("OSI")
VIs = meas(N, cont_mob, a)
Vs = avg(VIs[0])
Is = avg(VIs[1])
Rs = R(Vs[0],Is[0],Vs[1],Is[1])

instr.write("O")

scc = (sum(Rn[2])-sum(Rs[2]))/8


#def gain(Vt,instrs, G = 0, H = 255):
#    instrs[3].write("G"G) #set gain G
#    instrs[3].write("H"H) #set gain H
#    instrs[1].write("S12") #set source contact probes
#    instrs[1].write("M34") #set measurement contact probes
#    u = abs(Vt/(float(instrs[3].read())/(256/H))) #ratio of target voltage Vt to measured voltage 
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

G = gain(2,instrs)
gain(2, instrs,G[0],G[1])

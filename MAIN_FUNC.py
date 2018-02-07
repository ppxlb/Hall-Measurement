# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:27:14 2017

@author: ppxlb
"""

import numpy as np
import tkinter as tk
from SETUP import set_up
from INSTRS import initialise
from GAIN import gain
from MEAS import meas, meas_vdp
from PROCESS import avg, R
from CHCK import chck
from RESIST import resistivity
from HALL import Hall

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
"""----------GUI SETUP---------"""
window = tk.Tk()

ent = []
dft = ["100","3","5","0.5"]
for i in range(0,4):
    ent.append(tk.Entry(window))
    ent(i).delete(0,tk.END)
    ent(i).insert(0,dft(i))
    ent(i).pack()
#I_ent = tk.Entry(window)
#I_ent.delete(0,tk.END)
#I_ent.insert(0,"100")
#I_ent.pack()
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
Txt = tk.Text(window,wrap=tk.WORD,yscrollcommand=scrollbar.set,height = 45, width = 70)
Txt.pack(side=tk.RIGHT)

"""-------------------------contacts definitions--------------------------"""

cont_Ra = np.array([[43,12],[34,21],[12,43],[21,34]])
cont_Rb = np.array([[23,14],[32,41],[41,32],[14,23]]) #Both of these require ADVANCED indexing
cont_Rm = np.array([[31,42],[13,24],[42,13],[24,31]])

dline = "--------------------------------------------------"

#I = float(I_ent.get())
#I = float(input("Current (uA): "))
#N = int(round(float(input("Sampling Count: "))))
#t = float(input("thickness (um): "))
#t_err = float(input("thickness error (um): "))

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""


"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

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

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""



#output2 = resistivity(a,gain,meas_vdp,avg,R,N,G)
#add in: resistance calculation, takes 1st array divides by second.
#Averaging and SD func that works for any array so we can have <V>, <I>, <R_test>, Ra and Rb
#set script so that we run the tests, do an average, print/check agreement

"""~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

#h = Hall(a, gain, meas_vdp, avg, R, N, I, G)
#Rs = output2[0]
#mob = 1/((h[2]*Rs)*(1.602*10**-19))
#mob_err = mob*(np.sqrt(((Rs_err/Rs)**2)+(RH_err/h[2])))
#print ("Hall Mobility: ", "%e" % mob, chr(177), "cm^2/Vs") #"%.g" % mob_err,
    

chck_btn = tk.Button(window, text = "Check contacts", command = lambda : chck(meas, avg, a, dline, N, Txt, tk) )
chck_btn.pack(side=tk.LEFT)
shres_btn = tk.Button(window, text = "Resistivity Measurement", command = lambda : resistivity(a, meas_vdp, avg, R, N, G, dline, t, t_err, Txt, tk))
shres_btn.pack(side=tk.LEFT)
mob_btn = tk.Button(window, text = "Hall Measurement", command = lambda : Hall(a, gain, meas_vdp, avg, R, N, I, G, dline, t, t_err, Txt, tk) )
mob_btn.pack(side=tk.LEFT)
window.title("HALL 9000")
window.geometry("1200x800")
window.wm_iconbitmap("HALL9000.ico")
window.mainloop()

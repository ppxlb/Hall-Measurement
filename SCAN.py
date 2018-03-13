# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 14:48:27 2018

@author: localadmin
"""
import matplotlib.pyplot as plt

def scan (instrs, gain, meas, Ii,If, step,Txt,tk):
    V = []
    Io = []
    If += step
    cont = (12,34)
    for x in range(int(Ii),int(If),int(step)):
        instrs[2].write("I"+str(x))
        G = gain(1,instrs)        
        instrs[1].write("S"+str(cont[0])) #set source contact probes
        instrs[1].write("M"+str(cont[1])) #set measurement contact probes
        instrs[3].write("G"+str(G[0]))
        instrs[3].write("H"+str(G[1]))
        V.append(abs(float(instrs[3].read())/((255/G[1])*10**G[0]))) #read volatage in to some variable, insert to our arrays
        Io.append(float(instrs[2].read())) #read current in to some variable
#    Txt.insert(tk.END, "Highest gain at "+str(Io[V.index(max(V))]+"\n"))
#    Txt.insert(tk.END, "Lowest gain at "+str(Io[V.index(min(V))]+"\n"))
    plt.plot(Io,V,'x')
    plt.plot(Io[V.index(max(V))],max(V))
    plt.plot(Io[V.index(min(V))],min(V))
    plt.ylabel('Voltage (V)')
    plt.xlabel('Current (uA)')
    plt.title('IV scan from '+str(Ii)+'uA to '+str(If-step)+'uA')
    plt.show()

def winscan(instrs, gain, meas,scan,Txt,tk):
    window2 = tk.Tk()
    Iilabel = tk.Label(window2, text="Start current (uA):")
    Iilabel.place(x=5,y=5,width=120,height=25)
    Ii_ent = tk.Entry(window2)
    Ii_ent.place(x=125,y=5,width=120,height=25)
    Iflabel = tk.Label(window2, text="End current (uA):")
    Iflabel.place(x=5,y=30,width=120,height=25)
    If_ent = tk.Entry(window2)
    If_ent.place(x=125,y=30,width=120,height=25)
    stplabel = tk.Label(window2, text="Step size (uA):")
    stplabel.place(x=5,y=55,width=120,height=25)
    stp_ent = tk.Entry(window2)
    stp_ent.place(x=125,y=55,width=120,height=25)
    go = tk.Button(window2,text="Scan", command = lambda : scan(instrs, gain, meas, float(tk.Entry.get(Ii_ent)),float(tk.Entry.get(If_ent)), float(tk.Entry.get(stp_ent)),Txt,tk))
    go.place(x=125,y=85)
    window2.title("Current Scan")
    window2.geometry("370x160+2+2")
    window2.wm_iconbitmap("HALL9000.ico")
    window2.mainloop()
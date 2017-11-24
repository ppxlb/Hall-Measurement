# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:26:10 2017

@author: ppxlb
"""
import numpy as np

def R_stats (arr_R,N):
    cont_av = np.empty(6)#individual contacts average
    cont_sd = np.empty(6)#standard deviations for 6 contact averages
    for i in range(0,6):
        cont_av[i]=np.mean(arr_R[i])
        cont_sd[i]=np.std(arr_R[i])
    tot_av = np.mean(cont_av)#overall average
    tot_sd = np.mean(cont_sd)#overall standard deviation
    return cont_av,cont_sd, tot_av,tot_sd
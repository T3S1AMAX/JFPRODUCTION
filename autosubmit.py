#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 13:13:56 2022
@author: teslamax
"""
import numpy as np
import re
import sys
import os
'''
SRUN THIS FILE AT THE BOTTOM OF YOUR RUN SCRIPT
'''
#open your output file
fout=open('relax.out','r')
#open your input file
fin=open('scf.in','r')
line=fout.readline()
energy=[]
#set your expected accuracy
diff=1e-6
line2=[]
DATA=[]
while line:
    line1=line.split()
    if len(line1)>=1:
        if line1[0]=='!':
            print(line1[-2])
            energy.append(line1[-2])
        if line1[0]=='CELL_PARAMETERS':
            for i in range (0,9):
                line2.append(line)
                line=fout.readline()
            line1=line.split()
            if len(line)<=2:
                line2=[]
            elif line1[0]!='End' and line1[1]!='final':
                line2=[]
    line=fout.readline()
if len(line2)<=8:
    print("not converged")
elif len(energy)>1:
    print("converged")
    cdiff=abs(eval(energy[-1])-eval(energy[-2]))
    if cdiff>diff:
        print("start another calculation")
        LINE=fin.readline()
        while LINE:
            LINE1=LINE.split()
            if len(LINE1)>=1:
                if LINE1[0]=='CELL_PARAMETERS':
                    for i in range (0,9):
                        DATA.append(line2[i])
                        LINE=fin.readline()
                else:
                    DATA.append(LINE)
                    LINE=fin.readline()
            else:
                DATA.append(LINE)
                LINE=fin.readline()
        fin.close()
        fin=open('scf.in','w')
        for i in range (0,len(DATA)):
            fin.write(DATA[i])
        fin.close()
        #sbatch your run script
        os.system("sbatch run1.qe")
    else:
        print("no more calculations needed")
else:
    print("converged")
    print("no more calculations needed")
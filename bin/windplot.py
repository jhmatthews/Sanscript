#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 
import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import matplotlib.cm as cmap
import numpy as np
from math import *


str_ion=str(raw_input('Ion species to plot:'))


fname=sys.argv[1]+".ion"+str_ion+'.dat'
plotname=sys.argv[1]+".ion"+str_ion+'_plot.png'
i=0
input_file=open(fname, 'r')
X=[]; Y=[]; IP_array=[]
for line in input_file:
	i+=1	
	if i>3:
		x,y,IP=line.split()
		X.append(float(x))
		Y.append(float(y))
		IP=float(IP)
		if IP==0.0: 
			IP_array.append(-1000000.0)
		else:
			IP_array.append(log(IP))

X=np.array(X)
Y=np.array(Y)
#IP=np.array(IP)
print IP_array
plt.contourf(X,Y,IP,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
plt.colorbar()

plt.savefig(plotname)
os.system('open -a preview '+plotname)






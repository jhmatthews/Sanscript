#!/usr/bin/env python -i --pylab
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import pylab as p

#################################

#Simple potting program for column data
#syntax plot file n m
#run in interactive mode!

#################################
def save():
	savename=str(raw_input('Enter savename:'))
	p.savefig(savename)
	os.system('open -a preview '+ savename)

#Function to read a file
def plotit(arg, m, n):
	columns=np.loadtxt(arg, dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)

	m=int(m)
	n=int(n)

	columns=np.transpose(columns)

	x=np.array(columns[m])
	y=np.array(columns[n])

	#fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	#ax=fig.add_subplot(1,1,1)
	p.plot(x,y)
	return x,y

def sh():
	p.show()

def loadit(arg, m, n):
	columns=np.loadtxt(arg, dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)

	m=int(m)
	n=int(n)
	columns=np.transpose(columns)

	x=np.array(columns[m])
	y=np.array(columns[n])
	return x, y, columns


#savename=sys.argv[1]+'_plotcol.png'
#plt.savefig(savename)
#os.system('open -a preview '+ savename)


	
#################################




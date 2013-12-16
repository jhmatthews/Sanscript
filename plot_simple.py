#!/usr/bin/env python -i
import numpy as np
import matplotlib.pyplot as plt
import os, sys

#################################

#Simple potting program for n column data
#syntax plot file n
#run in interactive mode!

#################################

#Function to read a file
def read(filename):
	x,y=[],[]
	names=[]
	fileread=open(filename, 'r')
	plot=True
	for string in sys.argv:
		if string=='sum': plot=False
	for line in fileread:
		data=line.split()
		if len(data)>1:
			if data[1]=='Freq.': names=data[2:len(data)+1]
		if data[0]!='#':
			n_col=len(data)-1
			x.append(float(data[0]))
			temp=[]
			for i in range(n_col):
				temp.append(float(data[i+1]))
			y.append(temp)

	if len(names)==0: names=np.empty(len(y))
	arr=np.array(y)
	x=np.array(x)
	y=np.transpose(arr)
	print names


	for i in range(len(y)): print names[i], np.sum(y[i])
	return names,x, y

#Function which prints out sums of columns
def prt(names22,x22,y22):
	print 'x',  np.sum(x22)
	for i in range(len(y22)): print names22[i], np.sum(y22[i])

#Function which plots outcolumns
def pl(x2,y2):
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	for i in range(n_col):
		print i
		lab=str(raw_input('Enter label:'))
		ax=fig.add_subplot(n_col,1,i+1)
		ax.plot(x2,y2[i], label=lab)
		ax.legend()
	

	savename=sys.argv[1]+'_plot.png'
	plt.savefig(savename)
	os.system('open -a preview '+ savename)

def pset():
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	ax=fig.add_subplot(1,1,1)
	return ax

def add(xxx,yyy,ax):
	ax.plot(xxx,yyy)
	plt.savefig('temp.png')
	os.system('open -a preview temp.png')
	
#################################

#Now do actual code
plot=True
for string in sys.argv:
	if string=='sum': plot=False

#x,y=np.loadtxt(sys.argv[1], dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)


#CARRY OUT ABOVE FUNCTION
names_vals,x_vals,y_vals=read(sys.argv[1])


if plot: 
	pl(x_vals,y_vals)



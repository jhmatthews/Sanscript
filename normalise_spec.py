#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 

#--------------------------------------------------------
#This is a python sceript which normalises a spec file and outputs it to another file without the header, but with same column formats
#
#JM
#
#----------------------------------------------------------


import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np
import subroutines as subrtn
from raw_str import raw


tempspec=[]
restofspecfile=[]
no_obs=True
input_filename=sys.argv[1]
if 'spec' in sys.argv[1]:
	input_filename=sys.argv[1]
else:
	input_filename=sys.argv[1]+'spec'

output_filename='norm_'+input_filename

f=open(input_filename, 'r')
out=open(output_filename, 'w')

for line in f:
	data=line.split()
	if len(data)>0:
		if data[0]=='#' or data[0]=='#Freq.':
			if (data[2]=="no_observers"): 
				nobs=int(data[3])
				no_obs=False
		else:
			tempspec.append(data[8:len(data)])
			restofspecfile.append(data[0:7])

if no_obs:
	nobs=int(raw_input('No observers?? How many!??:'))


for i in range(len(tempspec)):
	for j in range(len(tempspec[i])):
		tempspec[i][j]=float(tempspec[i][j])


spec=np.transpose(tempspec)
rest=np.transpose(restofspecfile)

delta_norm=1
print 'normalising spectra.'
for i in range(nobs):
	#normalisation_flux=sum(smoothspec[i])/len(smoothspec[i])
	spec[i]=subrtn.normalise(spec[i], delta_norm)

output_array=[]
#tempspec=np.transpose(spec)

print len(spec), len(rest)

for j in range(len(spec[0])):
	for i in range(len(rest)):
		out.write(str(rest[i][j])+' ')
		
	for i in range(len(spec)):	
		out.write(str(rest[i][j])+' ')
	
	out.write('\n')







#---------------------------------------------------------------------------------
#	JM 25/02/13
#
# This is workhorse.py: 
# a load of useful plotting and file reading routines to do bulk work.
#
#---------------------------------------------------------------------------------

#import modules used directly in these routines:
import sys, os
import matplotlib.pyplot as plt
import numpy as np
import subroutines as subrtn
from raw_str import raw

#---------------------------------------------------------------------------------

#	spectot_plot
#
#	This function plots data from a spec_tot file when supplied with 
#	certain arguments.

def spectot_plot(*args, **kwargs):
	print len(args)
	titlearr=['Emitted', 'CenSrc', 'Disk', 'Wind', 'HitSurf','Scattered']
	color=['g','b', 'r', 'k', 'c', 'm', 'y']
	n=int(kwargs['plot'])
	bin=int(kwargs['bin'])
	comp=str(kwargs['comp'])
	l1=float(kwargs['l1'])
	l2=float(kwargs['l2'])
	ny=int(kwargs['ny'])
	nx=int(kwargs['nx'])
	log=bool(kwargs['log'])
	fname=str(kwargs['fname'])
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	fig.suptitle(fname,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	if comp=='True':
		for i in range(n+2):
			ax=fig.add_subplot(ny,nx,i)
			plt.xlim(l1,l2)
			if i==1:
				plt.xlim(l1,l2)
				if log: ax.set_xscale('log')
				if log: ax.set_yscale('log')
				ax.set_title(titlearr[i],fontsize=14)
				for j in range(len(args)):
					ax.plot(args[j].wavelength[0:-bin],args[j].CenSrc, c=color[j])	
			if i<2: 
				plt.xlim(l1,l2)
				if log: ax.set_xscale('log')
				if log: ax.set_yscale('log')
				ax.set_title(titlearr[i],fontsize=14)
				for j in range(len(args)):
					ax.plot(args[j].wavelength[0:-bin],args[j].CenSrc, c=color[j])

	else:
		for i in range(n+2):
			ax=fig.add_subplot(ny,nx,i)
			if i<2: 
				plt.xlim(lmin,lmax)
				if log: ax.set_xscale('log')
				if log: ax.set_yscale('log')
				ax.set_title(titlearr[i],fontsize=14)
				for j in range(len(args)):
					ax.plot(args[j].wavelength[0:-bin],arg[j].CenSrc, c=color[j])


#	spec_plot
#
#	This function plots data from various viewing angles for a .spec file when supplied with 
#	certain arguments.



#	specsources_plot
#
#	This function plots data for the sources for a .spec file when supplied with 
#	certain arguments.




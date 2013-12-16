#! /bin/bash

#--------------------------------------------------------
# 	yso_spectot.py
# intended to plot spectot files
#
#       JM 15/02/13
#----------------------------------------------------------


#import general modules
import sys, os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

#These modules are self written for plotting Python with Python..(see what I did there?)
import workhorse as wh
import write as wrt
import subroutines as subrtn
from raw_str import raw
import plotit as pltit

#print os.environ['PATH']


#Get started-----------------------------------------------

#set rcparams in matplotlib
wh.setpars()
wh.printit()

print 'Hi there, let\'s make some plots'
print '------------------------------\n\n'

no_obs=True
format='jpg'

#Initialise mode, store and spectot classes with arrays
mode=wh.initmode()
spectot=wh.initspectot()
spectot2=wh.initspectot()
store=wh.initstore()

t_spectot=wh.initspectot()
t_spectot2=wh.initspectot()


#read system arguments and set modes. set values to store.
wh.read_args(sys.argv, mode, store)



#-------------------------------------------------------------------------------
# IF IN SUPERMONGO MODE
if mode.sm:
	print 'you are in supermongo mode!'
	format='jpg'


	fname_read=False
	which_to_plot=[]
	labels_to_plot=[]
	inp_cmd =open(fname_cmd,'r')
	print 'INPUTS:\n'
	for line in inp_cmd.readlines():
		data=line.split()
		if len(data)>1:
			print data[0], data[1]
			if data[0]=='fname': 
				fname=str(data[1])+'.spec'
				savename=str(data[1])
				fname_read=True
				main_title=fname
			if data[0]=='lmin': lmin=float(data[1])
			if data[0]=='lmax': lmax=float(data[1])
			if data[0]=='norm': 
				if data[1]==1: normalised=True
			if data[0]=='plot': which_to_plot.append(int(data[1]))
			if data[0]=='label': labels_to_plot.append(data[1])
			if data[0]=='title': main_title=data[1]
			if data[0]=='xlabel': xlab=data[1]
			if data[0]=='ylabel': ylab=data[1]
			if data[0]=='rcparamstr': plt.rcParams[data[1]] = data[2]
			if data[0]=='rcparamint': plt.rcParams[data[1]] = int(data[2])
			if data[0]=='rcparamfl': plt.rcParams[data[1]] = float(data[2])
	
			if data[0]=='store.ibin': store.ibin=int(data[1])
			if data[0]=='format': format=data[1]

	if fname_read:
		inp =open(fname,'r')
	else: 
		if 'spec' in sys.argv[1]:
			fname=sys.argv[1]
		else:
			fname=sys.argv[1]+".spec"
		savename=sys.argv[1]
		inp =open(fname,'r')

if mode.comp or mode.resid:
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	if 'spec' in sys.argv[2]:
		fname2=sys.argv[2]
	else:
		fname2=sys.argv[2]+".spec"
		
	store.ibin=int(sys.argv[3])
	print fname, ' compared against ', fname2
else:
	#first open file 1
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	store.ibin=int(sys.argv[2])
	print fname




#Initialise arrays -----------------------------------------------------------------------

#tempspec=[]
#tempspec2=[]
i=-1
fmax=[0,0,0,0,0,0,0,0,0,0,0]
fmin=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]
fmax2=[0,0,0,0,0,0,0,0,0,0,0]
fmin2=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]

#------------------------------------------------------------------------------

# READ IN DATA FROM SPEC_TOT FILE
#
# These routines are located in workhorse.py
#

print 'Reading data from .spec_tot file.'
wh.read_spectotfile(fname, t_spectot)

#if you are in comparison or residual mode, open file 2 and read

if mode.comp or mode.resid:
	print 'Reading data from', fname2, 'for comparison.'
	no_obs=True
	wh.read_spectotfile(fname2, t_spectot2)
	
print 'Data read.'

#-------------------------------------------------------------------------------------

if mode.range:
	lmin=store.lmin_arg
	lmax=store.lmax_arg
	print 'you are plotting in range ', lmin, lmax

#Smooth spectrum and prepare for plotting.
print 'smoothing spectrum.'
print 'smoothing factor is ', store.ibin


#we smooth out the arrays
wh.smooth_preparetot(t_spectot, spectot, store) 
wh.smooth_preparetot(t_spectot2, spectot2, store) 

save_suffix='spectot'


wh.makespectotnumpy(spectot)
wh.makespectotnumpy(spectot2)



print len(spectot.CenSrc), len(spectot.wavelength[0:-store.ibin])

#------------------------------------------------------------------------------------	
#Sources plot
if mode.sources:
	print 'Now plotting sources with matplotlib.'
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	fig.suptitle(fname,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=8

	if mode.resid:
		spectot.Emitted=spectot.Emitted-spectot2.Emitted
		spectot.CenSrc=spectot.CenSrc-spectot2.CenSrc
		spectot.Disk=spectot.Disk-spectot2.Disk
		spectot.Wind=spectot.Wind-spectot2.Wind
		spectot.HitSurf=spectot.HitSurf-spectot2.HitSurf
		spectot.Scattered=spectot.Scattered-spectot2.Scattered


	ax=fig.add_subplot(2,1,1)
	plt.xlim(lmin,lmax)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	ax.set_title("CenSrc",fontsize=14)
	ax.plot(spectot.wavelength[0:-store.ibin],spectot.CenSrc, c='g')
	if mode.comp: 
		ax.plot(spectot.wavelength[0:-store.ibin],spectot2.CenSrc, c='b')
		plt.rcParams['text.color']='green'
		plt.text(0.5*(float(lmin+lmax)),2.0e-11,fname,fontsize=10)
		plt.rcParams['text.color']='blue'
		plt.text(0.5*(float(lmin+lmax)),3.0e-11,fname2,fontsize=10)
		plt.rcParams['text.color']='black'
	plt.xlim(lmin,lmax)
	ax=fig.add_subplot(2,1,2)
	plt.xlim(lmin,lmax)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	ax.set_title("Disk",fontsize=14)
	ax.plot(spectot.wavelength[0:-store.ibin],spectot.Disk, c='g')
	if mode.comp: ax.plot(spectot.wavelength[0:-store.ibin],spectot2.Disk, c='b')
        plt.xlim(lmin,lmax)	
	save=wrt._files(fname, mode, store, 2)


#spectotcomp_plot(2, lmin, lmax,
pltit.spectot_plot(spectot, spectot2, l1=lmin, l2=lmax, ny=3, nx=2, comp=mode.comp, plot=4, bin=store.ibin, fname=fname, log=mode.log)
save=wrt._files(fname, mode, store, 2)

os.system('open -a preview '+save)

#ALL DONE

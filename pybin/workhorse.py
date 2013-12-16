
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

#import function
'''def imports():
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	from constants import *
	import numpy as np
	import csv, sys, os, array, warnings, subprocess
	import pywind_sub as ps
	import math as mth
	import subroutines as subrtn
	from raw_str import raw
'''
#---------------------------------------------------------------------------------

#set standard JM rcparams for matplotlib.pyplot module
def setpars():
	print 'setting rcParams'
	plt.rcParams['lines.linewidth'] = 1.0
	plt.rcParams['axes.linewidth'] = 1.3
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = 'Times New Roman'
	plt.rcParams['text.usetex']='True'
	print 'you are setting params'
	return 0


#set rcparams according to some mode for matplotlib.pyplot module
def setparsmode():
	print 'setting rcParams'
	plt.rcParams['lines.linewidth'] = 1.5
	plt.rcParams['axes.linewidth'] = 1.3
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = 'Times New Roman'
	return 0

def printit():
	print 'Hello World.'
	return 0


#---------------------------------------------------------------------------------



#DEFINE SOME CLASSES


#mode class: sets mode from command line
class modeclass:
	'''The mode class: for reading arguments from command line'''
	def __init__(self, smmode, normmode, compmode, sourcesmode, mxmode, logmode, residmode, relative_resmode, helpmode, vlinesmode, rangemode):
		self.sm=smmode
		self.norm=normmode
		self.comp=compmode
		self.sources=sourcesmode
		self.mx=mxmode
		self.log=logmode
		self.resid=residmode
		self.relative_res=relative_resmode
		self.help=helpmode
		self.vlines=vlinesmode
		self.range=rangemode
		#self.name=instancename

#store class: sets stored valuesfrom command line
class stored_args:
	'''This is a class for storing any values read from the command line'''	
	def __init__(self, lminptr, lmaxptr, fnamecmdptr, maxy, ibinptr, filestore, titlestore):
		self.lmin=lminptr
		self.lmax=lmaxptr
		self.ibin=ibinptr
		self.fnamecmd=fnamecmdptr
		self.maximum_y=maxy
		self.filename=filestore
		self.title=titlestore

#spectot class: arrays of values read from spectot files
class spectotclass:
	'''This is a class for storing any values read from a spec_tot files'''	
	def __init__(self, emit, cen, dis, win, scat, hit, fre, wave):
		self.Emitted=emit
		self.CenSrc=cen
		self.Disk=dis
		self.Wind=win
		self.Scattered=scat
		self.HitSurf=hit
		#self.titles=title
		self.freq=fre
		self.wavelength=wave


class specclass:
	'''This is a class for storing any values read from a spec_tot files'''	
	def __init__(self, emit, cen, dis, win, scat, hit, fre, wave, title, temp, temp2, temp3, temp4):
		self.Emitted=emit
		self.CenSrc=cen
		self.Disk=dis
		self.Wind=win
		self.Scattered=scat
		self.HitSurf=hit
		self.titles=title
		self.freq=fre
		self.wavelength=wave
		self.tempspec=temp
		self.smoothtempspec=temp2
		self.spec=temp3
		self.smoothspec=temp4

class topbase_class:
	'''This is a class for topbase photoionization data'''	
	def __init__(self, nz, ne, islp_init, E0_init, linit, np_init, energies, cross_sections):
		self.Z = nz
		self.ion = ne
		self.islp = islp_init
		self.l = linit
		self.E0 = E0_init 
		self.np = np_init
		self.energy = energies
		self.XS = cross_sections

#---------------------------------------------------------------------------------
#Functions to initialise above classes.
#usage: classname=workhorse.initclass()

def initmode():
	modecl=modeclass(False, False, False, False, False, False, False, False,False, True, False)
	return modecl

def initstore():
	storecl=stored_args(0,0,0,0,0,0,0)
	return storecl

def initspectot():
	'''Initialises spectot arrays'''
	print 'Initialising spec_tot arrays.'	
	spectot=spectotclass([],[],[],[],[],[], [], [], [])
	return spectot

def initspec():
	'''Initialises spec arrays'''
	print 'Initialising spec arrays.'	
	spec=spectotclass([],[],[],[],[],[], [], [], [], [], [], [], [],[], [], [], [])
	return spec

def read_topbase(filename_read):
	## first initialise the class
	top = topbase_class([],[],[],[],[],[], [], [])

	## read the summary records into the topbase class
	top.Z,top.ion,top.islp,top.l,top.E0,top.np = sum_records = np.loadtxt( filename_read,
	            dtype={'names': ('Z', 'ion', 'islp', 'l', 'E0', 'np'),
	            'formats': ('i4', 'i4', 'i4', 'i4', 'float', 'i4')},
	                        comments='PhotTop ', delimiter=None, converters=None,
	                        skiprows=0, usecols=(1,2,3,4,5,6), unpack=True, ndmin=0)

    ## then read the actual cross sections into temporary arrays
	energy, XS = np.loadtxt(filename_read, dtype='float',
	                        comments='PhotTopS', delimiter=None, converters=None,
	                        skiprows=0, usecols=(1,2), unpack=True, ndmin=0) 

	## then read the temporary arrays into the class
	lower = 0

	for i in range(len(top.Z)):
		upper = lower + top.np[i]
		top.energy.append(energy[lower:upper])
		top.XS.append(XS[lower:upper])
		lower = upper

	top.energy = np.array ( top.energy )
	top.XS = np.array ( top.XS )
	return top


def read_topbase_orig(filename_read):
	## first initialise the class
	top = topbase_class([],[],[],[],[],[], [], [])

	## read the summary records into the topbase class
	filetoread= open(filename_read, 'r')
	for line in filetoread:
		data = line.split()
		if data[0] == 'PhotTopS':
			top.Z.append(float(data[1]))
			top.ion.append(float(data[2]))
			top.islp.append(float(data[3]))
			top.l.append(float(data[4]))
			top.E0.append(float(data[5]))
			top.no.append(float(data[6]))

	top.Z=np.array(top.Z)
	top.ion=np.array(top.ion)
	top.islp=np.array(top.islp)
	top.l=np.array(top.l)
	top.E0=np.array(top.E0)
	top.np=np.array(top.np)
			

    ## then read the actual cross sections into temporary arrays
	energy, XS = np.loadtxt(filename_read, dtype='float',
	                        comments=('PhotTopS','#'), delimiter=None, converters=None,
	                        skiprows=0, usecols=(1,2), unpack=True, ndmin=0) 

	## then read the temporary arrays into the class
	lower = 0

	for i in range(len(top.Z)):
		upper = lower + top.np[i]
		top.energy.append(energy[lower:upper])
		top.XS.append(XS[lower:upper])
		lower = upper

	top.energy = np.array ( top.energy )
	top.XS = np.array ( top.XS )
	return top


def get_topbase_filename(letter):
	if letter=='h1' or letter=='h': f = 'topbase_h1_phot.py'
	if letter=='he1' or letter=='he': f = 'topbase_he1_phot.py'
	if letter=='he2': f = 'topbase_he2_phot.py'
	if letter=='c' or letter=='n' or letter =='o': f = 'topbase_cno_phot.py'	
	if letter=='fe': f = 'topbase_fe_phot.py'
	filename = 'data/atomic73/'+f
	return filename

def get_z(letter):
	if letter=='h1' or letter=='h': z=1
	if letter=='he1' or letter=='he' or letter=='he2': z = 2
	if letter=='c': z = 6
	if letter=='n':  z = 7
	if letter =='o':  z = 8
	if letter=='fe': z = 26
	return z

#---------------------------------------------------------------------------------

#functions to convert all arrays in spec class to numpy arrays

def makespecnumpy(speccl):
	'''Converts spectot arrays'''
	print 'Converting spec_tot arrays to numpy.'	
	speccl.Emitted=np.array(speccl.Emitted)
	speccl.CenSrc=np.array(speccl.CenSrc)
	speccl.Disk=np.array(speccl.Disk)
	speccl.Wind=np.array(speccl.Wind)
	speccl.Scattered=np.array(speccl.Scattered)
	speccl.HitSurf=np.array(speccl.HitSurf)
	speccl.freq=np.array(speccl.freq)
	speccl.wavelength=np.array(speccl.wavelength)
	speccl.smoothtempspec=np.array(speccl.smoothtempspec)
	speccl.tempspec=np.array(speccl.tempspec)
	speccl.smoothspec=np.array(speccl.smoothspec)
	speccl.spec=np.array(speccl.smoothtempspec)

#functions to convert all arrays in spectot class to numpy arrays
def makespectotnumpy(spectotcl):
	'''Converts spectot arrays'''
	print 'Converting spec_tot arrays to numpy.'	
	spectotcl.Emitted=np.array(spectotcl.Emitted)
	spectotcl.CenSrc=np.array(spectotcl.CenSrc)
	spectotcl.Disk=np.array(spectotcl.Disk)
	spectotcl.Wind=np.array(spectotcl.Wind)
	spectotcl.Scattered=np.array(spectotcl.Scattered)
	spectotcl.HitSurf=np.array(spectotcl.HitSurf)
	spectotcl.freq=np.array(spectotcl.freq)
	spectotcl.wavelength=np.array(spectotcl.wavelength)

	
#---------------------------------------------------------------------------------	

#Reading arguments from command line

def read_args(sysargv, modea, stored1):
	'''This function reads arguments from the command line'''
	print 'reading arguments.'
	if (len(sysargv)<3):
		stored1.ibin=1
	for i in range(len(sysargv)):
		if sysargv[i]=='-s': 
			modea.sm=True
			stored1.fname_cmd=sysargv[i+1]
		if sysargv[i]=='-n': 
			modea.norm=True
		if sysargv[i]=='-r': 
			modea.range=True
			stored1.lmin_arg=float(sysargv[i+1])
			stored1.lmax_arg=float(sysargv[i+2])
		if sysargv[i]=='-c': 
			modea.comp=True
		if sysargv[i]=='-nc': 
			modea.norm=True
			modea.comp=True	
		if sysargv[i]=='-res': 
			modea.resid=True
		if sysargv[i]=='h': 
			modea.help=True
			dummy=help_me()
		if sysargv[i]=='-rel': 
			modea.resid=True
			modea.relative_res=True
		if sysargv[i]=='nolines': 
			modea.vlines=False
		if sysargv[i]=='sources': 
			modea.sources=True
		if sysargv[i]=='-log': 
			modea.log=True
			#lmin_log=float(sysargv[i+1])
			#lmax_log=float(sysargv[i+2])
		if sysargv[i]=='-max':
			modea.mx=True
			stored1.maximum_y=float(sysargv[i+1])
		if sysargv[i]=='-name':
			stored1.filename=sysargv[i+1]
		if sysargv[i]=='-title':
			stored1.title=sysargv[i+1]
	return 0


#---------------------------------------------------------------------------------
#read in from a specfile

def read_specfile(fname, t_spectot):
	'''Reads from a .spec file and appends to arrays'''
	no_obs=True
	inp=inp =open(fname,'r')
	for line in inp.readlines():
		if (len(line)>4):
			if (line[0]=='#'):
				data=line.split()
				#print data[2]
				if (data[2]=="lum_agn(ergs/s)"): lpl=float(data[3])
				elif (data[2]=="agn_power_law_index"): alpha=float(data[3])
				elif (data[2]=="rstar(cm)"): 
					rbb=float(data[3])
					disk_radmin=float(data[3])
				elif (data[2]=="tstar"): tbb=float(data[3])
				elif (data[2]=="Star_radiation(y=1)"): istar=int(data[3])
				elif (data[2]=="Disk_radiation(y=1)"): idisk=int(data[3])
				elif (data[2]=="QSO_BH_radiation(y=1)"): ibh=int(data[3])
				elif (data[2]=="disk.mdot(msol/yr)"): disk_mdot=float(data[3])
				elif (data[2]=="disk.radmax(cm)"): disk_radmax=float(data[3])
				elif (data[2]=="mstar(msol)"): mbh=float(data[3])		
				elif (data[2]=="no_observers"): nobs=int(data[3])
				elif (data[2]=="no_observers"): no_obs=False
				elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
				elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
				elif (data[1]=="Freq."):
					titles[0:len(line)-2]=data[1:len(line)-1]
			else:
				data=line.split()
				t_spectot.freq.append(data[0])
				t_spectot.wavelength.append(data[1])
				t_spectot.Emitted.append(data[2])
				t_spectot.CenSrc.append(data[3])
				t_spectot.Disk.append(data[4])
				t_spectot.Wind.append(data[5])
				t_spectot.HitSurf.append(data[6])
				t_spectot.Scattered.append(data[7])
				if no_obs:
					nobs=int(raw_input('No observers?? How many!??:'))
					no_obs=False


#---------------------------------------------------------------------------------
#smooth and prepare arrays from a SPEC file

def smooth_prepare(t_spectot, spectot, store): 
	for i in range(len(t_spectot.Emitted)-store.ibin):
		temp1=[]
		for j in range(nobs):
			temp=0.0
			t1=t2=t3=t4=t5=t6=0.0
			for k in range(store.ibin):
				t1=t1+float(t_spectot.Emitted[i+k])
				t2=t2+float(t_spectot.CenSrc[i+k])
				t3=t3+float(t_spectot.Disk[i+k])
				t4=t4+float(t_spectot.Wind[i+k])
				t5=t5+float(t_spectot.HitSurf[i+k])
				t6=t6+float(t_spectot.Scattered[i+k])
			t1=t1/bin
			t2=t2/bin
			t3=t3/bin
			t4=t4/bin
			t5=t5/bin
			t6=t6/bin
		spectot.Emitted.append(t1)
		spectot.CenSrc.append(t2)
		spectot.Disk.append(t3)
		spectot.Wind.append(t4)
		spectot.HitSurf.append(t5)
		spectot.Scattered.append(t6)
#---------------------------------------------------------------------------------


#read in from a spectotfile

def read_spectotfile(fname, t_spectot):
	no_obs=True
	inp=inp =open(fname,'r')
	for line in inp.readlines():
		if (len(line)>4):
			if (line[0]=='#'):
				data=line.split()
				#print data[2]
				if (data[2]=="lum_agn(ergs/s)"): lpl=float(data[3])
				elif (data[2]=="agn_power_law_index"): alpha=float(data[3])
				elif (data[2]=="rstar(cm)"): 
					rbb=float(data[3])
					disk_radmin=float(data[3])
				elif (data[2]=="tstar"): tbb=float(data[3])
				elif (data[2]=="Star_radiation(y=1)"): istar=int(data[3])
				elif (data[2]=="Disk_radiation(y=1)"): idisk=int(data[3])
				elif (data[2]=="QSO_BH_radiation(y=1)"): ibh=int(data[3])
				elif (data[2]=="disk.mdot(msol/yr)"): disk_mdot=float(data[3])
				elif (data[2]=="disk.radmax(cm)"): disk_radmax=float(data[3])
				elif (data[2]=="mstar(msol)"): mbh=float(data[3])		
				elif (data[2]=="no_observers"): nobs=int(data[3])
				elif (data[2]=="no_observers"): no_obs=False
				elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
				elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
				elif (data[1]=="Freq."):
					t_spectot.titles[0:len(line)-2]=data[1:len(line)-1]
			else:
				data=line.split()
				t_spectot.freq.append(data[0])
				t_spectot.wavelength.append(data[1])
				t_spectot.Emitted.append(data[2])
				t_spectot.CenSrc.append(data[3])
				t_spectot.Disk.append(data[4])
				t_spectot.Wind.append(data[5])
				t_spectot.HitSurf.append(data[6])
				t_spectot.Scattered.append(data[7])
				if no_obs:
					nobs=int(raw_input('No observers?? How many!??:'))
					no_obs=False


#---------------------------------------------------------------------------------

#smooth and prepare arrays from a spectotfile
def smooth_preparetot(t_spectot, spectot, store): 
	for i in range(len(t_spectot.Emitted)-store.ibin):
		t1=t2=t3=t4=t5=t6=0.0
		bin=float(store.ibin)
		for k in range(store.ibin):
			t1=t1+float(t_spectot.Emitted[i+k])
			t2=t2+float(t_spectot.CenSrc[i+k])
			t3=t3+float(t_spectot.Disk[i+k])
			t4=t4+float(t_spectot.Wind[i+k])
			t5=t5+float(t_spectot.HitSurf[i+k])
			t6=t6+float(t_spectot.Scattered[i+k])
		t1=t1/bin
		t2=t2/bin
		t3=t3/bin
		t4=t4/bin
		t5=t5/bin
		t6=t6/bin
		spectot.Emitted.append(t1)
		spectot.CenSrc.append(t2)
		spectot.Disk.append(t3)
		spectot.Wind.append(t4)
		spectot.HitSurf.append(t5)
		spectot.Scattered.append(t6)
	spectot.wavelength=t_spectot.wavelength
	spectot.titles=t_spectot.titles
	spectot.freq=t_spectot.freq

#---------------------------------------------------------------------------------

#Make six arrays into numpy arrays

def make_numpy(arr1, arr2, arr3, arr4, arr5, arr6):
	arr1=np.array(arr1)
	arr2=np.array(arr2)
	arr3=np.array(arr3)
	arr4=np.array(arr4)
	arr5=np.array(arr5)
	arr6=np.array(arr6)

#---------------------------------------------------------------------------------

def help_me():
	help_string=''' You want help...ok...
		        usage genplot filename 
				Args: [ibin] [-n] [-s sm_commands] [-r lmin lmax] [-c] [nolines] [sources] [-log] [-max]
				      [-max] [-res] [-rel]

 		        -n means normalised
			-s means SM mode (you 
			-r means specify lmin and lmax
			-c means comparison mode
			-res means residual mode
			-rel means relative residuals
			-log means logmode
			-max means set the maximum y value to one
			nolines means no lines
			sources means also plot sources for spectra e.g. CenSrc, Emitted.
			This program will now exit, you can rerun!.\n
			'''
	
	print help_string
	sys.exit()
	return 0


def help_me_more():
	help_string=''' You want more help...ok...
		        usage genplot filename [ibin] [-n] [-s sm_commands] [-r lmin lmax] [-c] [nolines] [sources]
 		        -n means normalised
			-s means SM mode (you 
			-r means specify lmin and lmax
			-c means comparison mode
			-res means residual mode
			-rel means relative residuals
			nolines means no lines
			sources means also plot sources for spectra e.g. CenSrc, Emitted.
			This program will now exit.\n
			'''
	print help_string
	sys.exit()
	return 0

#---------------------------------------------------------------------------------

############################################
#
#	JM, 15/03/13
#
#	spectotsub
#
#  python routine that reads in spectra
#  from spectot or logspectot file and puts it 
#  in a class SPEC
#
#
############################################

import numpy as np
import workhorse as wh
import sys, os
from constants import *



def readspectot(fname):
	spec=wh.spectotclass
	arr=np.loadtxt(fname, dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
	arr=np.transpose(arr)
	spec.Emitted=arr[2]
	spec.CenSrc=arr[3]
	spec.Disk=arr[4]
	spec.Wind=arr[5]
	spec.Scattered=arr[6]
	spec.HitSurf=arr[7]
	spec.freq=arr[0]
	spec.wavelength=arr[1]
	return spec




def readspec(fname):
	spec=wh.spectotclass
	arr=np.loadtxt(fname, dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
	arr=np.transpose(arr)
	spec.Emitted=arr[2]
	spec.CenSrc=arr[3]
	spec.Disk=arr[4]
	spec.Wind=arr[5]
	spec.Scattered=arr[6]
	spec.HitSurf=arr[7]
	spec.freq=arr[0]
	spec.wavelength=arr[1]
	return spec
	
def readspeclum(fname):
	normalise=4.0*PI*((100.0*PC)**2)
	spec=wh.spectotclass
	arr=np.loadtxt(fname, dtype='float', comments='#', delimiter=None, converters=None, skiprows=0, usecols=None, unpack=False, ndmin=0)
	arr=np.transpose(arr)
	spec.freq=arr[0]
	spec.wavelength=arr[1]
	#print spec.freq, spec.wavelength
	for i in range(2,8):
		dlambd=spec.wavelength[1]-spec.wavelength[0]
		for j in range(len(spec.wavelength)):	
			arr[i][j]=arr[i][j]*normalise*dlambd	
			if j<len(spec.wavelength)-1: dlambd=spec.wavelength[j]-spec.wavelength[j+1]
	spec.Emitted=arr[2]
	spec.CenSrc=arr[3]
	spec.Disk=arr[4]
	spec.Wind=arr[5]
	spec.Scattered=arr[6]
	spec.HitSurf=arr[7]
	#print len(spec.Disk), len(spec.CenSrc), len(spec.wavelength)
	return spec

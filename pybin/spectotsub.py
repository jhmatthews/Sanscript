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



	

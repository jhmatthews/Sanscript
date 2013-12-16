
import math as mth
import numpy as np
#import subroutines as subrtn
#from raw_str import raw
import workhorse as wh
from constants import *

#---------------------------
#18/02/2013- J Matthews
#
#Useful Physics functions Module
#
#---------------------------

#All in CGS units

def planck_lambda(temperature,wavelength):
	'''Planck function. requires kelvin and cm as input, returns specific intensity B_nu'''
	I=((2.0*H*(C**2)) / (wavelength**5)) * (1.0/( np.exp((H*C)/(wavelength*BOLTZMANN*temperature)) - 1.0 ))
	return I

def planck_nu(temperature,nu):
	'''Planck function. requires kelvin and Hz as input, returns specific intensity B_nu'''
	I=((2.0*H*(C**2)) / (wavelength**5)) * (1.0/( np.exp((H*C)/(wavelength*BOLTZMANN*temperature)) - 1.0 ))
	return I

def RJ(temperature,wavelength):
	'''Rayleigh jeans law, wavelength. requires kelvin and cm as input, returns specific intensity B_nu'''
	RJ_out=(2.0*C*BOLTZMANN*temperature)/(wavelength**4)
	return RJ_out

def Wien_law(temp):
	lambda_max=0.29 * temp
	return lambda_max
	
def SB(temp):
	F= STEFAN_BOLTZMANN * (temp**4)
	return F













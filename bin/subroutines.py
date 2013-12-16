#-------------------------------

#JM 11.12.12

#Useful python subroutines

#-------------------------------

import csv, sys, os, array, warnings
import numpy as np
import math as mth


#Find the mean of an array x, ignoring points a certain distance away

def mean_with_ignore(x,delta_ignore):
	"""take the mean, then ignore points, x_i that satisfy (x_i-mean)/mean>delta. if delta_ignore=0 use original mean."""
	sum_over_x=sum(x)
	mean_x=( 1.0 * sum(x) )  /  ( 1.0 * len(x) )
	x_no_outliers=[]
	if delta_ignore!=0:
		for i in range(len(x)):
			test_val= (x[i])/mean_x
			if test_val<=delta_ignore: x_no_outliers.append( x[i] )	
		mean_no_outliers=( 1.0 * sum(x_no_outliers) )  /  ( 1.0 * len(x_no_outliers) )
		return mean_no_outliers
	else: 
		return mean_x


def normalise(x, delta):
	"""normalise data so 1=mean (including ignoring any outliers if specified. if delta_ignore=0 use original mean."""
	mean_norm=mean_with_ignore(x,delta)
	x_normalised=[]
	for i in range(len(x)):
		x_norm= 1.0 * x[i] / mean_norm
		x_normalised.append(x_norm)
	return x_normalised

def find_mean_no_variability(x, y, grad_crit):
	"""ignore points that have changed from the last point by more than dy/dx=grad_crit"""
	baseline=[]
	for i in range(len(x)-1):
		delta_x = x[i+1] - x[i]
		delta_y = y[i+1] - y[i]
		dy_by_dx=delta_y/delta_x
		if dy_by_dx<grad_crit: baseline.append( y[i+1] )
	
	return baseline


def write_files(x,y, filename):
	"""writes two arrays to a file"""
	file_writing=open(filename, 'w')
	for i in range(len(x)):
		file_writing.write(str(x[i])+'  '+str(y[i])+'\n')
	


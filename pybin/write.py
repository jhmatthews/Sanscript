
#-----------------------------------------------
# 	JM 25/02/13
#
# Modules for writing jpg files from plots.
#
#
#-----------------------------------------------

import sys, os
import matplotlib.pyplot as plt
import numpy as np
#import subroutines as subrtn
#from raw_str import raw
import workhorse as wh


#code for writing files out of plotting routines.


def _files(filename2, mode, stored, source_or_spec):
	if '.spec_tot' in filename2: 
		filename=filename2[0:-9]
	elif '.spec' in filename2: 
		filename=filename2[0:-5]
	else:
		filename=filename2
	if mode.comp: save_suffix='comp'
	if mode.resid: save_suffix='resid'
	if mode.sm: save_suffix='sm'
	if mode.log: save_suffix='log'
	if source_or_spec==0:
		if mode.range:
			#save spectrum sources figure with range given	
			savename=filename+"_range"+str(stored.lmin_arg)+"_"+str(stored.lmax_arg)+'_'+save_suffix+'spec_summary.jpg'
			plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

		else:
			#save spectrum sources figure
			savename=filename+'_'+save_suffix+'spec_summary.jpg'
			plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')
	else:
		if mode.range:
			#save spectrum sources figure with range given	
			savename=filename+"_range"+str(stored.lmin_arg)+"_"+str(stored.lmax_arg)+'_'+save_suffix+'sources.jpg'
			plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

		else:
			#save spectrum sources figure
			savename=filename+'_'+save_suffix+'sources.jpg'
			plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')
	
	print 'Files saved as', savename
	return savename


def _output(sysargv, n_obs, wavelength, smoothspec):
	yno=str(raw_input('do you want to write to file y/n?'))
	orig_filename=sysargv[1]
	if yno=='y':
		for i in range(nobs):
			filename=orig_filename+'_fileoutput'+str(i+1)
			subrtn.write_files(wavelength[0:-store.ibin], smoothspec[i], filename)
	return 0
	

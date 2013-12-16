#----------------------------------------------------------

#This is a script to create pf files from an initial pf file, 
#including pywind plots and onepage spectrum plots.

#----------------------------------------------------------

import csv, sys, os, array, warnings, subprocess
import time

fname=sys.argv[1]			#initial filename specified as system argument
old_file=open(fname+'.pf','r')

num_pfs=int(raw_input('Number of new files:'))

array_params_orig=[]
array_values_orig=[]

i_line=0
for line in old_file:
	params,values=line.split()
	array_params_orig.append(params)	
	array_values_orig.append(values)
	print params

pf_files=[]
for it in range(num_pfs):
	temp_params=array_params_orig
	temp_values=array_values_orig
	Editing=True
	new_filename=str(raw_input('Enter a new_filename:'))
	pf_files.append(new_filename)
	new_file=open(new_filename+'.pf','w')
	while Editing:
		parameter=str(raw_input('What would you like to edit:'))
		if parameter=='n': Editing=False
		if Editing: 
			new_value=str(raw_input('What value should it have:'))
			for i in range(len(temp_params)):
				#print temp_params[i], parameter
				if temp_params[i]==parameter:
					temp_values[i]=new_value
					print 'changed\n'
	
	for i in range(len(temp_params)): new_file.write(temp_params[i]+'	'+temp_values[i]+'\n')
	new_file.close()



old_file.close()

scr_filename=str(raw_input('Enter a script filename:'))
scr_file=open(scr_filename,'w')

curdir=str(os.getcwd())

scr_file.write('cd '+curdir+'\n\n')
for i in range(num_pfs):
	scr_file.write('py '+pf_files[i]+' > '+pf_files[i]+'.out &\n')


scr_file.write('\nwait\n')
scr_file.close()
				
		
		
	
	


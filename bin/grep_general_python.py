
#---------------------------------------------------------------------

#			SOUTHAMPTON UNIVERSITY

#JM 12/12/12

#This is a code which makes a web of python dependencies

#--------------------------------------------------------------------

#import modules of use
import sys, os, time, subprocess
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab 
import numpy as np
import math as mth
import random
#import subroutines as subrtn
plt.rcParams['lines.linewidth'] = 0.4
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['font.family'] = 'serif'
fig=plt.figure(figsize=(8.3,11.7),dpi=80)
ax = fig.add_subplot(111)

template_file=open('templates.h','r')
template_file_array=[]
for line in template_file:  #We go through templates.h to find what functions are contained in each c file.
		functions=line.split()
		template_file_array.append(functions)
c_called_by=[]
c_functions_in=[]
ran_y_coords=[]

#name files, the c file is given as a cmd line argument



#do an ls in folder to get all the c files.
#capture output to array all_c_files, and strip newline characters.
proc = subprocess.Popen(['ls *.c'], stdout=subprocess.PIPE, shell=True)
all_c_files=proc.stdout.readlines()
all_c_files = map(lambda s: s.strip(), all_c_files) 

for i_c_file in range(len(all_c_files)):
	code_filename=all_c_files[i_c_file]
	outside_code_file=True
	functions_in_code_file=[]
	functions_called_by_code=[]
	print 'going through template file and grepping....'
	for i in range(len(template_file_array)):  #We go through templates.h to find what functions are contained in each c file.
		functions=template_file_array[i
]

		if outside_code_file:		# we are not in the list of functions in code_filename
			if functions[0]=='/*':
				if functions[1]==code_filename:
					outside_code_file=False		#we have reached the start of the list of functions

			else:
				#if outside code file then do a grep for said function in our code_filename
				#if we find it we put it an array for later.
				grep_int=os.system('grep '+functions[1]+' '+code_filename+ ' > temp_log_file &')
				if grep_int==0:
					functions_called_by_code.append(functions[1])




		else:
			if functions[0]=='/*': 		# we have reached the end of the list of functions
				outside_code_file=True
			else: 				# append these functions to a list
				functions_in_code_file.append(functions[1])
	


	c_called_by.append(functions_called_by_code)
	c_functions_in.append(functions_in_code_file)
	#remove the output file of the grep.		
	i=os.system('rm -f temp_log_file') 
	ran_y=random.random()*len(all_c_files)
	if all_c_files[i_c_file]=='python.c': ran_y=0.0
	ran_y_coords.append(ran_y)
	print ran_y
	



x=[0, 1]
y=[0, 1]
colors=['b', 'g', 'm', 'y','k','r', 'c']
print 'getting there'

print len(all_c_files), len(c_called_by), len(c_functions_in)
#print len(c_called_by[10]), len(c_functions_in[10])
print c_called_by
for i_c_file in range(len(all_c_files)):
	print i_c_file
	c_string=colors[int(random.random()*7)]
	for i in range(len(c_called_by[i_c_file])):
		j=0
		found=0
		while j<len(all_c_files) and found==0:
			for k in range(len(c_functions_in[j])):
				if c_called_by[i_c_file][i]==c_functions_in[j][k]:
					found=1
					#print 'found'
					x=[j, i_c_file]
					y=[ran_y_coords[j], ran_y_coords[i_c_file]]
					ax.plot(x, y, c=c_string)
					
			j+=1

ax.set_autoscale_on(False)
ax.set_xlim(0,104)
ax.set_ylim(0,104)
ax.set_title('Python Map- points connect linked c files')
plt.savefig('/Users/jmatthews/Dropbox/tree_python_2.png')
plt.show()


#All done for that file.
#NOW attempt at more general code to find links between codes (maybe try plotting as well??)


	






















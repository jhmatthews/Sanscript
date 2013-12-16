
#---------------------------------------------------------------------

#			SOUTHAMPTON UNIVERSITY

#JM 12/12/12

#This is a quick code which prints out all the functions in a  C file
#and also prints out the functions that that C file calls.
#could be used to make a 'web' of python?

#--------------------------------------------------------------------

#import modules of use
import sys, os, time, subprocess
#import matplotlib.pyplot as plt
import numpy as np
#import subroutines as subrtn


#name files, the c file is given as a cmd line argument
code_filename=sys.argv[1]+'.c'
template_file=open('templates.h','r')

outside_code_file=True
functions_in_code_file=[]
functions_called_by_code=[]


proc = subprocess.Popen(["ls *.c"], stdout=subprocess.PIPE, shell=True)
all_c_files=proc.stdout.readlines()
#(out, err) = proc.communicate()
all_c_files = map(lambda s: s.strip(), all_c_files)
print "program output:", all_c_files



print 'going through template file and grepping....'

for line in template_file:  #We go through templates.h to find what functions are contained in each c file.
	functions=line.split()

	if outside_code_file:		# we are not in the lsit of functions in code_filename
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
	





#remove the output file of the grep.		
i=os.system('rm -f temp_log_file') 
	



#now just print statements.
print '\n\n--------------------------------------\n'
print 'This is a list of the functions in '+code_filename+':\n'

for i in range(len(functions_in_code_file)):
	print functions_in_code_file[i]+'\n'			

print '\n\n--------------------------------------'

time.sleep(10)

print 'This is a list of the functions CALLED by '+code_filename

for i in range(len(functions_called_by_code)):
	print functions_called_by_code[i]+'\n'

print '\n\n--------------------------------------'

#All done.




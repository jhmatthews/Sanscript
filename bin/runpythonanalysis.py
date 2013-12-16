
#----------------------------------------------------------

#This is a script to run analysis of PYTHON, 
#including pywind plots and onepage spectrum plots.

# 22/11/12: Edited program, as initially it specified a number of lines as an argument
# this improvement means it can now know the number of runs via if statement.

#this code  


#----------------------------------------------------------

#import modules
import csv, sys, os, array, warnings, subprocess
import numpy as np
import time

#we read in the script used to run the files as the argument.
#syntax: python runpythonanalysis.py hamann_script_01 lin 20 [no] [no]
test_array=sys.argv
fname=sys.argv[1]		#filename specified as argument
lin_log=sys.argv[2]		#whether to plot pywind as linear or log space.	
smooth=sys.argv[3]		#smoothing factor for spectra

script_file=open(fname,'r')	#open the file used to submit iridis job

#variable to count lines in script file, and array of pf filenames
line_counter=0			
filenames=[]


#depending on [no] [no] being present then we rerun scripts, or not.
if len(sys.argv)==5: 
	print 'OK, you don\'t want to rerun\
		pywind_lin_summary and spectrum_onepage.\
		Let\'s view the plots...'

if len(sys.argv)==6: 
	print 'OK, you don\'t want to rerun\
		pywind_lin_summary and spectrum_onepage\
		 or view the plots, so let\'s create TeX.'

num_runs=0
#----------------------------------------------------------
#read in script file to get filenames
if len(sys.argv)<6: print 'OK, making plots.\n'
for line in script_file:
		#go through the script file line by line
	line_counter=line_counter+1
	if len(sys.argv)<6: print 'Progress: '+str(line_counter-1)+' out of '+str(num_runs)+'\n'
	
	arr_line=line.split()
	if len(arr_line)>1:
		str1=arr_line[0]
		pf_filename=arr_line[1]
		if str1=='py':
			num_runs=num_runs+1
			cmdline='python ~/Documents/Analysis_Scripts/pywind_lin_summary.py '+pf_filename+' '+lin_log+' > pywind_output'
			if len(sys.argv)<6: 
				try:
					subprocess.check_call(cmdline,shell=True)
				except:
					pass	
				#run pywind plotting script if wanted

			cmdline='python ~/Documents/Analysis_Scripts/spectrum_onepage_new.py '+pf_filename+' '+smooth
			
			if len(sys.argv)<6: 
				try:
					subprocess.check_call(cmdline,shell=True)
				except:
					pass
				#run spectra plotting script if wanted

			filenames.append(pf_filename)	#put filenames in array




#----------------------------------------------------------
#view jpg files generated, if wanted

cmdline='open -a preview *hamann*.jpg &'
if len(sys.argv)<6: subprocess.check_call(cmdline,shell=True)

#----------------------------------------------------------
#now we create TeX files.


#determine if we are reading tex content from keyboard or file.
manual_or_existing=int(raw_input('would you like manual(0) or file(1) content mode for README?'))
if manual_or_existing==1: 
	content_filename=str(raw_input('Enter a content filename:')) 
	content_file=open(content_filename, 'r')

#table or description TeX format.
table_or_desc=int(raw_input('would you like table(0) or description(1) format for README?'))

#-------------------------------------------------------
#depending on variable produce table...

if table_or_desc==0:
	print 'OK, producing table tex file.'
	tabletex_file=open(fname+'.tex','w+')
	tabletex_file.write(r'''\documentclass{article}
\usepackage{pdflscape}
\begin{document}
\begin{landscape}
\begin{table}[h]
\centering
\begin{tabular}{| c | c |}
\hline
File & Comments  \\
\hline
''')

	if manual_or_existing==0:			#if manual content mode, enter comments on screen.
		for i in range(num_runs):
			pf_file=filenames[i]
			comments=str(raw_input('enter some comments for '+pf_file+' in TeX format:'))
			tabletex_file.write('$'+pf_file+'$'+' & '+comments+r' \\ '+'\n')

	if manual_or_existing==1:			#if file content mode, read in from file.
		for line in content_file:
			tabletex_file.write(line)
		


#end of TeX...		
	tabletex_file.write('''\hline
\end{tabular}
\caption{Readme table for $'''+fname+'''$ script }
\end{table}
\end{landscape}
\end{document}''')


#----------------------------------------------------------
#...or description


else:
	print 'OK, producing itemised description tex file.'
	tabletex_file=open(fname+'.tex','w+')
	tabletex_file.write(r'''\documentclass{article}
\begin{document}
\begin{description}
''')
	if manual_or_existing==0:			#if manual content mode, enter comments on screen.
		for i in range(num_runs):
			pf_file=filenames[i]
			comments=str(raw_input('enter some comments for '+pf_file+' in TeX format:'))
			tabletex_file.write('\item[$'+pf_file+'$]'+' '+comments+'\n')

	if manual_or_existing==1:			#if file content mode, read in from file.
		for line in content_filename:
			tabletex_file.write(line)


#end of TeX...	
	tabletex_file.write('''
\end{description}
\end{document}''')




#----------------------------------------------------------
#compile latex into pdf, and view.

try:
	cmdline='pdflatex '+fname+ '> latex_output &'
	i=os.system(cmdline)

	cmdline='open -a preview '+fname+'.pdf &'
	i=os.system(cmdline)

except:
	pass

#----------------------------------------------------------
#copy to dropbox, if user requires.

time.sleep(5)

dropbox=str(raw_input('would you like to copy these plots to dropbox (y/n)?'))
if dropbox=='y': 
	#create a folder in dropbox and copy these files over
	dropbox_mkdir=str(raw_input('Enter a sub directory to make in Dropbox/:'))
	dropbox_path='~/Dropbox/'+dropbox_mkdir
	i=os.system('mkdir '+dropbox_path)
	for it in range(len(filenames)):
		cmdline='cp '+filenames[it]+'*.jpg '+dropbox_path+'/'
		i=os.system(cmdline)
	cmdline='cp '+fname+'.pdf '+dropbox_path+'/'
	i=os.system(cmdline)

#quick clean-----
i=os.system('rm latex_output')
i=os.system('rm pywind_output')
i=os.system('rm  pyspec_output')


print '\n SCRIPT FINISHED.'
#----------------------------------------------------------
	






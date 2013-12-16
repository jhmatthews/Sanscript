#!/usr/bin/env python -i

import csv, sys, os, array, warnings, subprocess
from time import sleep
import urllib
#
cur_dir=os.getcwd()
py_dir='$PYTHON'
print cur_dir
#str_yn=str(raw_input('Correct directory y/n?'))

file_array=[]

if len(sys.argv)>1:
	str_ver=str(sys.argv[1])

	if str_ver=='help':
		print 'HELP?!?!?'


else:
	file_for_folders=open('/Users/jmatthews/Documents/Analysis_Scripts/folders', 'r')
	readme_template=open('/Users/jmatthews/Documents/Analysis_Scripts/README_template', 'r')
	for line in file_for_folders:
		readme_array=[]
		dummy_input_string='a string.'
		version_folder=line.split()[0]
		#readme_string=str(raw_input('Enter your read message below\n----------------------------\n,'))
		#print readme_string
		#print version_folder, len(version_folder)
		if len(version_folder)==10: version=version_folder[len(version_folder)-3: len(version_folder)-1]
		if len(version_folder)==18: version=version_folder[len(version_folder)-11: len(version_folder)-8]
		if len(version_folder)==17: version=version_folder[len(version_folder)-10: len(version_folder)-8]
		if len(version_folder)==19: version=version_folder[len(version_folder)-12: len(version_folder)-8]
		if len(version_folder)==22: version=version_folder[len(version_folder)-15: len(version_folder)-8]
		print 'VERSION RELEASE:', version, len(version_folder)

		#now we write to README file.
		readme_file=open('README.md', 'w')
		readme_file.write('README\n***\n=========\n')
		print 'Enter your read message below, type end when done\n----------------------------\n'
		while dummy_input_string!='end':
			dummy_input_string=str(raw_input(''))
			if dummy_input_string!='end':
				readme_file.write(dummy_input_string+'\n')


		for line in readme_template:
			readme_file.write(line)
		#page=urllib.urlopen("https://confluence.stsci.edu/display/StarWiki/PythonVersions")
		#data=page.read()
		#tempfile=open('tempfile', 'w')
		#tempfile.write(data)
		#os.system('open -a \'Google Chrome\' tempfile')
		#print data
		
				
		#sys.exit()
		os.system('git status')
		os.system('git checkout -B progs')
		os.system('rm -f *.c *.h *.o *~')
		os.system('rm -f Makefile')
		print 'Cleaned directory of previous files.'

		os.system('cp /Users/jmatthews/Downloads/python_downloads/'+version_folder+'*.c '+cur_dir+'/')
		os.system('cp /Users/jmatthews/Downloads/python_downloads/'+version_folder+'*.h '+cur_dir+'/')
		os.system('cp /Users/jmatthews/Downloads/python_downloads/'+version_folder+'Makefile '+cur_dir+'/')
		os.system('git add *.c')
		os.system('git add *.h')
		os.system('git add Makefile')
		os.system('git add README.md')
		os.system('git status')
		print 'Copied directory over and tracked files.'
		print 'Note that we only track .c, .h, Makefile and README.md when in this branch (progs)!'
		os.system('rm -f temp_file')
		str_yn2=str(raw_input('Proceed to Committing y/n?'))
		if str_yn2=='y':
			print 'Committing and pushing...'
			os.system('git commit -am "v'+version+' Commit"')
			os.system('git tag -a v'+version+' -m "Python '+version+' Release"')
		else: 
			print 'Nothing committed or tagged as something wrong...'
		str_yn2=str(raw_input('Push to server??'))
		if str_yn2=='y':
			os.system('git push origin progs')
			os.system('git push --tags')
		


		print 'All done.'



'''print 'Don\'t forget to bring your README.md file up to date with release!'
	print 'Also make sure you have no files that you don\'t want in this directory (this program will clean .h .c .o and Makefile if you want...'
	os.system('git checkout progs')
	str_yn2=str(raw_input('Clean files y/n? (WARNING: gets rid of all c, o, ~ and h files in this directory!!):'))
	if str_yn2=='y':
		os.system('rm -f *.c *.h *.o *~')
		os.system('rm -f Makefile')
		print 'Cleaned directory of previous files.'

        str_yn2=str(raw_input('Copy files from other directory?'))	
	if str_yn2=='y':
		os.system('ls -d /Users/jmatthews/Downloads/python_downloads/python_'+str_ver+'* > temp_file')
		fil=open('temp_file', 'r')
		for line in fil:                             7  5
			line_array=line.split()
			folder=str(line_array[0])
			file_array.append(folder)

		for i in range(len(file_array)): print file_array[i]

		if len(file_array)>1:
			folder_i=int(raw_input('Which one:')) - 1
			
		if len(file_array)==1: folder_i=0
		folder=file_array[folder_i]
		print folder
		print 'cp '+folder+'/*.c '+cur_dir+'/'
		os.system('cp '+folder+'/*.c '+cur_dir+'/')
		os.system('cp '+folder+'/*.h '+cur_dir+'/')
		os.system('cp '+folder+'/Makefile '+cur_dir+'/')
		os.system('git add '+cur_dir+'/*.c')
		os.system('git add '+cur_dir+'/*.h')
		os.system('git add '+cur_dir+'/Makefile')
		os.system('git add '+cur_dir+'/README.md')
		print 'Copied directory over and tracked files.'
		print 'Note that we only track .c, .h, Makefile and README.md when in this branch (progs)!'
	os.system('rm -f temp_file')
	str_yn2=str(raw_input('Proceed to Committing y/n?'))
	if str_yn2=='y':
		print 'Committing and pushing...'
		os.system('git commit -am "v'+str_ver+' Commit"')
		os.system('git tag -a v'+str_ver+' -m "Python '+str_ver+' Release"')
		os.system('git push origin progs')
		os.system('git push --tags')
	else: print 'Nothing committed or tagged as something wrong...'


print All done.'''





#!/usr/bin/env python -i

import csv, sys, os, array, warnings, subprocess
from time import sleep
#
cur_dir='$PYTHONGIT'
py_dir='$PYTHON'
print cur_dir
#str_yn=str(raw_input('Correct directory y/n?'))

file_array=[]

str_ver=str(sys.argv[1])

if str_ver=='help':
	print 'HELP?!?!?'


else:
	print 'Don\'t forget to bring your README.md file up to date with release!'
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
		for line in fil:
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


print 'All done.'





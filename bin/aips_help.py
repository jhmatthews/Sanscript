#!/usr/bin/env python -i

import csv, sys, os, array, warnings, subprocess

#three possible options. folder_to_home, folder_to_destination, file_to_home, file_to_destination 

if len(sys.argv)>1: fname=sys.argv[1]
folder_bool=False
destination_bool=False
help_bool=False

if len(sys.argv)==1: 
	print 'Error: Not enough arguments!!!' 
	help_bool=True

if len(sys.argv)==2:			# e.g. iridcp filename (just want to copy filename to hoem folder)
	folder_bool=False
	destination_bool=False
	if fname=='help': help_bool=True


if len(sys.argv)==3: 			# e.g. iridcp filename (just want to copy folder to home, or file to destination)
	if sys.argv[2]=='-r': 
		folder_bool=True
	 	destination_bool=False
	elif sys.argv[2]=='1': 
		folder_bool=True
	 	destination_bool=False
	else:
		folder_bool=False
	 	destination_bool=True
		destination=sys.argv[2]

if len(sys.argv)>3: 
	folder_bool=True
	destination_bool=True
	destination=sys.argv[2]


#change this to your use and home directory!!!
path_on_aips='jm8g08@152.78.192.83:/home/jm8g08/'

if help_bool:
	print 'You want help? Ok...'
	print 'to copy a file to astroaips home: aipscp path/filename'
	print 'to copy a file to astroaips destination: aipscp path/foldername path/on/aips/after/home/'
	print 'to copy a folder to astroaips home: aipscp path/foldername -r'
	print 'to copy a folder to astroaips destination: aipscp path/foldername path/on/aips/after/home/ -r'
	print 'to get this help message type aipscp help!'

else:
	if folder_bool:
		if destination_bool:
			cmdline='scp -r '+fname+' '+path_on_aips+destination
		else: 
			cmdline='scp -r '+fname+' '+path_on_aips

		print cmdline
		os.system(cmdline)

	else:
		if destination_bool:
			cmdline='scp '+fname+' '+path_on_aips+destination
		else:
			cmdline='scp '+fname+' '+path_on_aips
		print cmdline	
		os.system(cmdline)



print 'all done!'




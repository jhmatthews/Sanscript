import os, sys



os.system('ls -d ~/Documents/Python/progs/*python*/ > temp_file_list')

filename=open('temp_file_list', 'r')

i=0
for line in filename:
	arr=line.split()
	folder_name=str(arr[0])
	print_st='Cleaning Folder: '+folder_name+' .....'
	print print_st	
	os.system('rm -f '+folder_name+'*.o '+folder_name+'*~')
	print 'DONE.'

os.system('rm temp_file_list')
print 'All clean again!!\n'


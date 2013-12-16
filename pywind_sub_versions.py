
import numpy as np



def get_wind_geom(fname):
	x=[]
	z=[]
	lx=[]
	lz=[]
	xmax=0.0
	zmax=0.0
	inp =open(fname,'r')
	for line in inp.readlines():
		temp=line.split()
		if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
			if int(temp[5])==0:
				x.append(float(temp[0]))
				lx.append(np.log10(float(temp[0])+1))
			if int(temp[4])==0:
				z.append(float(temp[1]))
				lz.append(np.log10(float(temp[1])+1))
			if int(temp[3])>-1:
				xmax=float(temp[0])
				zmax=float(temp[1])
	ix=len(x)
	iz=len(z)
	print ix, iz
	return (ix,iz,x,z,lx,lz,xmax,zmax)



def get_wind_geom68(fname, coord_array):
	if len(coord_array)==0:
		coord_array=[]
		bool_68=False
	else: 
		bool_68=True
	x=[]
	z=[]
	lx=[]
	lz=[]
	xmax=0.0
	zmax=0.0
	inp =open(fname,'r')
	if bool_68:
		i=0
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				if coord_array[i][2]==0:
					x.append(float(temp[0]))
					lx.append(np.log10(float(temp[0])+1))
				if coord_array[i][1]==0:
					z.append(float(temp[1]))
					lz.append(np.log10(float(temp[1])+1))
				if coord_array[i][0]>-1:
					xmax=float(temp[0])
					zmax=float(temp[1])
				i=i+1
	else:
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				coord_array.append([int(temp[3]),int(temp[4]),int(temp[5])])
				if int(temp[5])==0:
					x.append(float(temp[0]))
					lx.append(np.log10(float(temp[0])+1))
				if int(temp[4])==0:
					z.append(float(temp[1]))
					lz.append(np.log10(float(temp[1])+1))
				if int(temp[3])>-1:
					xmax=float(temp[0])
					zmax=float(temp[1])
	ix=len(x)
	iz=len(z)
	return (ix,iz,x,z,lx,lz,xmax,zmax, coord_array)


def pywind_read(fname,x,z):
	array=np.empty([z,x])
	inp =open(fname,'r')
	for line in inp.readlines():
		temp=line.split()
		if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
			if int(temp[3])>-1:
				array[int(temp[5]),int(temp[4])]=float(temp[2])
			else:
				array[int(temp[5]),int(temp[4])]=-999
	output=np.ma.masked_equal(array,-999)

	return (output)

def pywind_read68(fname,x,z, coord_array):
	if len(coord_array)==0:
		coord_array=[]
		bool_68=False
	else: 
		bool_68=True
	array=np.empty([z,x])
	inp =open(fname,'r')
	if bool_68:
		i=0
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				#print fname, coord_array[i], i
				if int(coord_array[i][0])>-1:
					array[coord_array[i][2],coord_array[i][1]]=float(temp[2])
				else:
					array[coord_array[i][2],coord_array[i][1]]=-999
				i=i+1
	else:
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				coord_array.append([int(temp[3]),int(temp[4]),int(temp[5])])
				if int(temp[3])>-1:
					array[int(temp[5]),int(temp[4])]=float(temp[2])
				else:
					array[int(temp[5]),int(temp[4])]=-999

	output=np.ma.masked_equal(array,-999)
	#print output
	return output, coord_array




def pywind_log_read68(fname,x,z, coord_array):
	if len(coord_array)==0:
		coord_array=[]
		bool_68=False
	else: 
		bool_68=True
	array=np.empty([z,x])
	inp =open(fname,'r')
	line=inp.readline()
	line=inp.readline()
	if bool_68:
		i=0
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				if int(coord_array[i][0])>-1:
					array[coord_array[i][2],coord_array[i][1]]=np.log10(float(temp[2]))
				else:
					array[coord_array[i][2],coord_array[i][1]]=-999
				i=i+1
	else:
		for line in inp.readlines():
			temp=line.split()
			if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
				coord_array.append([int(temp[3]),int(temp[4]),int(temp[5])])
				if int(temp[3])>-1:
					array[int(temp[5]),int(temp[4])]=np.log10(float(temp[2]))
				else:
					array[int(temp[5]),int(temp[4])]=-999
	output=np.ma.masked_equal(array,-999)
	#if len(coord_array)>0: print 'coord: ', len(coord_array), len(coord_array[1])
	return output, coord_array







def pywind_read(fname,x,z, coord_array):
	if array==[0]: array=np.empty([z,x])
	inp =open(fname,'r')
	for line in inp.readlines():
		temp=line.split()
		if temp[0]!='ZONE' and temp[0]!='#' and temp[0]!='VARIABLES=' and temp[0]!='TITLE=':
			if int(temp[3])>-1:
				array[int(temp[5]),int(temp[4])]=float(temp[2])
			else:
				array[int(temp[5]),int(temp[4])]=-999
	output=np.ma.masked_equal(array,-999)

	return (output)





def pywind_log_read(fname,x,z):
	array=np.empty([z,x])
	inp =open(fname,'r')
	line=inp.readline()
	line=inp.readline()
	for line in inp.readlines():
		temp=line.split()
		if int(temp[3])>-1:
			array[int(temp[5]),int(temp[4])]=np.log10(float(temp[2]))
		else:
			array[int(temp[5]),int(temp[4])]=-999
	output=np.ma.masked_equal(array,-999)

	return (output)



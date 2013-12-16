#!/usr/bin/env python -i
import csv, sys, os, array, warnings, subprocess
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pywind_sub6874 as ps

#plt.rcParams[set_autoscale_on]='False'

fname=sys.argv[1]
vers=''
vers2=''
if len(sys.argv)>2: fname=sys.argv[1]
if len(sys.argv)>2: fname2=sys.argv[2]

if len(sys.argv)<4:
	cmdline='py_wind68g'+' '+fname2+' < ~/Documents/Analysis_Scripts/pywindcmds68g'
	subprocess.check_call(cmdline,shell=True)
	cmdline='py_wind74b4'+' '+fname+' < ~/Documents/Analysis_Scripts/pywindcmds68g'
	subprocess.check_call(cmdline,shell=True)	

	cmdline='py_wind68g'+' '+fname2+' < ~/Documents/Analysis_Scripts/pywindcmds68g2'
	subprocess.check_call(cmdline,shell=True)
	cmdline='py_wind74b4'+' '+fname+' < ~/Documents/Analysis_Scripts/pywindcmds68g2'
	subprocess.check_call(cmdline,shell=True)

x=[]
z=[]
x1=[]
z1=[]
lx=[]
lz=[]
lx1=[]
lz1=[]
data=[]
IPtemp=[]
tetemp=[]
nhtemp=[]
xtemp=[]
ztemp=[]
tetemp=[]
trtemp=[]
convtemp=[]
vx=[]
vz=[]
H1=[]
H2=[]
C4temp=[]
Si4temp=[]
N5temp=[]
O6temp=[]

tte=[[]]
coord_array=[]
coord_array2=[]
dummy=[]
ix,iz,x,z,lx1,lz1,xmax,zmax, coord_array=ps.get_wind_geom68(fname+'.ioncH1.dat',coord_array2)
lx, lz=lx1, lz1
ix2,iz2,x2,z2,lx2,lz2,xmax2,zmax2, dummy=ps.get_wind_geom68(fname2+'.ioncH1.dat',coord_array)
dummy=[]
first=True
for i in range(2):
	dummy2=dummy
	if i==0: 
		fname=fname
		coord_array=[]
		
	if i==1: 
		fname=fname2
		coord_array=dummy2
		first=False
		ix,iz,x,z,lx,lz,xmax,zmax=ix2,iz2,x2,z2,lx2,lz2,xmax2,zmax2
	#ix,iz,x,z,lx,lz,xmax,zmax,dummy=ps.get_wind_geom68(fname+'.ioncH1.dat',coord_array)
	H1,dummy=ps.pywind_read68(fname+'.ioncH1.dat',ix,iz, coord_array)
	H2,dummy=ps.pywind_read68(fname+'.ioncH2.dat',ix,iz, coord_array)

	H=np.empty([ix,iz])
	for i in range(ix):
		for j in range(iz):
			#if i==1: print H1[i][j], H2[i][j]
			H[i][j]=np.log10(H1[i][j]+H2[i][j])
			#if i==1: print 'total:', H[i][j]


	#IP=ps.pywind_read(fname+'.IP.dat',ix,iz)
	#vx=ps.pywind_read(fname+'.vrho.dat',ix,iz)
	#vz=ps.pywind_read(fname+'.vz.dat',ix,iz)
	#nagn=ps.pywind_log_read(fname+'.nphot.dat',ix,iz)
	C3,dummy=ps.pywind_log_read68(fname+'.ionC3.dat',ix,iz, coord_array)
	C4,dummy=ps.pywind_log_read68(fname+'.ionC4.dat',ix,iz, coord_array)
	C5,dummy=ps.pywind_log_read68(fname+'.ionC5.dat',ix,iz, coord_array)
	#C6,coords=ps.pywind_log_read(fname+'.ionC6.dat',ix,iz, coord_array)
	#ndisk=ps.pywind_log_read(fname+'.nphot.dat',ix,iz)
	te,dummy=ps.pywind_log_read68(fname+'.te.dat',ix,iz, coord_array)
	tr,dummy=ps.pywind_log_read68(fname+'.tr.dat',ix,iz, coord_array)
	#print dummy
	#vxz=np.empty([ix,iz])
	#for i in range(ix):
	#	for j in range(iz):
	#		vxz[i][j]=np.log10(np.sqrt(vx[i][j]*vx[i][j]+vz[i][j]*vz[i][j]))

	lx_scatter=[]
	lz_scatter=[]
	#These are the lines for reading in all the extra ions fraction
	for i_scatter in range(len(lx)):
		for i_scatter2 in range(len(lz)):
			if H[i_scatter][i_scatter2]>0:
				lx_scatter.append(lx[i_scatter2])
				lz_scatter.append(lz[i_scatter])


	if first: tte=te
	#print len(te[1]), te[1]

	lwind_scale=[lx1[1]-1,lx1[len(lx)-1],lz1[1]-1,lz1[len(lz)-1]]
	print lwind_scale
	wind_scale=[1e13,1e18,1e13,1e18]
	#print lwind_scale 
	#print wind_scale

	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	fig.suptitle(fname,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=8

	ax=fig.add_subplot(3,2,2)
	ax.set_autoscale_on(False)
	ax.set_title('log Hydrogen Density',fontsize=12)
	plt.axis(lwind_scale)
	plt.contourf(lx,lz,H,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	plt.colorbar()

	#ax=fig.add_subplot(3,2,3)
	#ax.set_autoscale_on(False)
	#ax.set_title('log Streamline velocity',fontsize=12)
	#plt.axis(lwind_scale)
	#plt.contourf(lx,lz,vxz,[5,6,7,8,9,10])
	#plt.colorbar()

	ax=fig.add_subplot(3,2,4)
	ax.set_autoscale_on(False)
	plt.axis(lwind_scale)
	ax.set_title('log Electron Temperature',fontsize=12)
	#print lx,lz,te
	#plt.scatter(lx_scatter,lz_scatter)
	plt.contourf(lx,lz,te,[3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])
	print lx
	plt.colorbar()
	#plt.scatter(lx_scatter,lz_scatter)

	ax=fig.add_subplot(3,2,6)
	ax.set_autoscale_on(False)
	plt.axis(lwind_scale)
	ax.set_title('Radiation temperature',fontsize=12)
	plt.contourf(lx,lz,tr,[3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])
	plt.colorbar()

	#ax=fig.add_subplot(3,2,2)
	#ax.set_autoscale_on(False)
	#plt.axis(lwind_scale)
	#ax.set_title('log Ionization parameter',fontsize=12)
	#plt.contourf(lx,lz,IP,[-4,-3,-2,-1,0,1,2,3,4,5,6,7])
	#plt.colorbar()

	#ax=fig.add_subplot(3,2,4)
	#ax.set_autoscale_on(False)
	#plt.axis(lwind_scale)
	#ax.set_title('log Number of AGN photons',fontsize=12)
	#plt.contourf(lx,lz,nagn,[0,1,2,3,4,5,6])
	#plt.colorbar()

	#ax=fig.add_subplot(3,2,6)
	#ax.set_autoscale_on(False)
	#plt.axis(lwind_scale)
	#ax.set_title('log Number of disk photons',fontsize=12)
	#plt.contourf(lx,lz,ndisk,[0,1,2,3,4,5,6,7,8,9,10])
	#plt.colorbar()

	cont=[-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0]

	ax=fig.add_subplot(3,2,1)
	ax.set_autoscale_on(False)
	plt.axis(lwind_scale)
	ax.set_title('log CIII proportion',fontsize=12)
	plt.contourf(lx,lz,C3,cont)
	plt.colorbar()

	ax=fig.add_subplot(3,2,3)
	ax.set_autoscale_on(False)
	plt.axis(lwind_scale)
	ax.set_title('log CIV proportion',fontsize=12)
	plt.contourf(lx,lz,C4,cont)
	plt.colorbar()

	ax=fig.add_subplot(3,2,5)
	ax.set_autoscale_on(False)
	plt.axis(lwind_scale)
	ax.set_title('log CV proportion',fontsize=12)
	plt.contourf(lx,lz,C5,cont)
	plt.colorbar()
	#ax=fig.add_subplot(3,2,7)
	#ax.set_autoscale_on(False)
	#plt.axis(lwind_scale)
	#ax.set_title('log CVI proportion',fontsize=12)
	#plt.contourf(lx,lz,C6,cont)
	#plt.colorbar()

	print 'saving figure'
	plt.savefig(fname+'geom_simple.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')




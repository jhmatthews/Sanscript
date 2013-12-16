#!/usr/bin/env python -i
import csv, sys, os, array, warnings, subprocess
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['axes.linewidth'] = 1.3
mpl.rcParams['font.family'] = 'serif'


fname=sys.argv[1]
ptype=1
if (len(sys.argv) > 2):
	if sys.argv[2] =='lin':
		ptype=2
	else:
		ptype=1

angles=[]

datafile=fname+'.spec_tot'
if (len(sys.argv) > 3 and os.path.exists(datafile)):
	dplot=sys.argv[3]
	inp =open(datafile,'r')
	for line in inp.readlines():
		if (len(line)>4):
			if (line[0]=='#'):
				data=line.split()
				print data[2][0:4]
				if (data[2]=="rstar(cm)"): 
					disk_radmin=float(data[3])
				elif (data[2]=="disk.radmax(cm)"): disk_radmax=float(data[3])
				elif (data[2]=="no_observers"): nobs=int(data[3])
				elif (data[2][0:5]=="angle"): angles.append(float(data[3]))
				elif (data[2][0:10]=="sv.diskmin"): svrmin=(float(data[3])*disk_radmin)
				elif (data[2][0:10]=="sv.diskmax"): svrmax=(float(data[3])*disk_radmin)
				elif (data[2][0:11]=="sv.thetamin"): samin=float(data[3])                             
				elif (data[2][0:11]=="sv.thetamax"): samax=float(data[3])
else:
	dplot=0

cmdline='py_wind '+fname+' < pywindcmds'


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
inwind=[]

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


#These are the lines for reading in the hydrogen densities
inp =open(fname+'.ioncH1.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
#temp=line.split()
#ix=int(temp[1][2:])
#iz=int(temp[2][2:])
for line in inp.readlines():
	temp=line.split()
	x.append(float(temp[0]))
	lx.append(np.log10(float(temp[0])+1))
	z.append(float(temp[1]))
	lz.append(np.log10(float(temp[1])+1))
	H1.append(float(temp[2]))
	if int(temp[3])>0:
		xmax=float(temp[0])
		lxmax=(np.log10(float(temp[0])+1))
		zmax=float(temp[1])
		lzmax=(np.log10(float(temp[1])+1))
	ix=int(temp[4])
	iz=int(temp[5])


ix=ix+1
iz=iz+1

inp =open(fname+'.ioncH2.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	H2.append(float(temp[2]))

Htemp=np.zeros(len(H1))
for i in range(len(H1)):
	Htemp[i]=H1[i]+H2[i]

#These are the lines for reading in temperatures
inp =open(fname+'.te.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	tetemp.append(float(temp[2]))

inp =open(fname+'.tr.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	trtemp.append(float(temp[2]))

#These are the lines for reading in velocities
inp =open(fname+'.vx.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	vx.append(float(temp[2]))

inp =open(fname+'.vz.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	vz.append(float(temp[2]))

vxztemp=np.zeros(len(vz))
for i in range(len(vz)):
	vxztemp[i]=np.sqrt(vx[i]*vx[i]+vz[i]*vz[i])


#These are the lines for reading in all the extra ions fractions
inp =open(fname+'.ionC4.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	C4temp.append(float(temp[2]))

inp =open(fname+'.ionSi4.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	Si4temp.append(float(temp[2]))

inp =open(fname+'.ionN5.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	N5temp.append(float(temp[2]))

inp =open(fname+'.ionO6.dat','r')
line=inp.readline()
line=inp.readline()
#line=inp.readline()
for line in inp.readlines():
	temp=line.split()
	O6temp.append(float(temp[2]))

#OK, all data inputs complete, we now reshape data to form matrices for plotting
#We need two blocks, because depending or whether you request lin or log output, x and z are different
if x[0]==x[1]:
	z1=z[0:iz]
	lz1=lz[0:iz]
	H=np.log10(np.transpose(np.reshape(Htemp,(ix,iz))))
	te=np.log10(np.transpose(np.reshape(tetemp,(ix,iz))))
	tr=np.log10(np.transpose(np.reshape(trtemp,(ix,iz))))
	vxz=np.log10(np.transpose(np.reshape(vxztemp,(ix,iz))))
	C4=np.log10(np.transpose(np.reshape(C4temp,(ix,iz))))
	Si4=np.log10(np.transpose(np.reshape(Si4temp,(ix,iz))))
	N5=np.log10(np.transpose(np.reshape(N5temp,(ix,iz))))
	O6=np.log10(np.transpose(np.reshape(O6temp,(ix,iz))))
	for i in range(ix):
		x1.append(x[i*iz])
		lx1.append(np.log10(x[i*iz]))
else:
	x1=x[0:ix]
	lx1=lx[0:ix]
	H=np.log10(np.reshape(Htemp,(ix,iz)))
	te=np.log10(np.reshape(tetemp,(ix,iz)))
	tr=np.log10(np.reshape(trtemp,(ix,iz)))
	vxz=np.log10(np.reshape(vxztemp,(ix,iz)))
	C4=np.log10(np.reshape(C4temp,(ix,iz)))
	Si4=np.log10(np.reshape(Si4temp,(ix,iz)))
	N5=np.log10(np.reshape(N5temp,(ix,iz)))
	O6=np.log10(np.reshape(O6temp,(ix,iz)))
	for i in range(iz):
		z1.append(z[i*ix])
		lz1.append(np.log10(z[i*ix]))



lwind_scale=[lx1[1],lxmax,lz1[0],lzmax]
wind_scale=[0,xmax,0,zmax]

fig=plt.figure(figsize=(11.7,8.3),dpi=80)
fig.suptitle(fname,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=8
ax=fig.add_subplot(1,1,1)
ax.set_title('log Hydrogen Density',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,H,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,H,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	if (dplot > 0):
		plt.plot([disk_radmin,disk_radmax],[0,0],linewidth=10)
		plt.plot([svrmin,xmax],[0,(xmax-svrmin)*np.tan(np.radians(90.0-samin))],color='r')
		plt.plot([svrmax,xmax],[0,(xmax-svrmax)*np.tan(np.radians(90.0-samax))],color='g')
		for ang in angles:
			plt.plot([0,xmax],[0,xmax*np.tan(np.radians(90.0-ang))],color='k')

plt.colorbar()
plt.savefig(fname+'lingeometry_summary.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

fig=plt.figure(figsize=(8.3,11.7),dpi=80)
fig.suptitle(fname,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=8


ax=fig.add_subplot(4,2,1)
ax.set_title('log Hydrogen Density',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,H,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,H,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	if (dplot > 0):
		for ang in angles:
			plt.plot([0,xmax],[0,xmax*np.tan(np.radians(90.0-ang))],color='k')
			plt.plot([disk_radmin,disk_radmax],[0,0],linewidth=10)
plt.colorbar()

ax=fig.add_subplot(4,2,3)
ax.set_title('log Streamline velocity',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,vxz,[5,6,7,8,9,10])
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,vxz,[5,6,7,8,9,10])
plt.colorbar()

ax=fig.add_subplot(4,2,5)
ax.set_title('log Electron Temperature',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,te,[4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,te,[4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])
plt.colorbar()


ax=fig.add_subplot(4,2,7)
ax.set_title('Radiation temperature',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,tr,[4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,tr,[4,4.2,4.4,4.6,4.8,5.0,5.2,5.4,5.6,5.8,6,6.2,6.4,6.6,6.8,7])	
plt.colorbar()


cont=[-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0]

ax=fig.add_subplot(4,2,2)
ax.set_title('log CIV proportion',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,C4,cont)
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,C4,cont)
plt.colorbar()

ax=fig.add_subplot(4,2,4)
ax.set_title('log SiIV proportion',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,Si4,cont)
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,Si4,cont)
plt.colorbar()

ax=fig.add_subplot(4,2,6)
ax.set_title('log NV proportion',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,N5,cont)
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,N5,cont)
plt.colorbar()

ax=fig.add_subplot(4,2,8)
ax.set_title('log OVI proportion',fontsize=12)
if ptype==1:
	plt.axis(lwind_scale)
	plt.contourf(lx1,lz1,O6,cont)
else:
	plt.axis(wind_scale)
	plt.contourf(x1,z1,O6,cont)
plt.colorbar()


plt.savefig(fname+'lingeometry.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')



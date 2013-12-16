#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 
import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np

titles=[]
freq=[]
wavelength=[]
emitted=[]

star_bl=[]
disk=[]
wind=[]
hitsurf=[]
scattered=[]
tempspec=[]
i=-1
fmax=[0,0,0,0,0,0,0,0,0,0,0]
fmin=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]



if (len(sys.argv)<3):
	ibin=1
else:
	ibin=int(sys.argv[2])

fname=sys.argv[1]+".spec"




print fname
inp =open(fname,'r')
for line in inp.readlines():
	if (len(line)>4):
		if (line[0]=='#'):
			data=line.split()
			print data[2]
			if (data[2]=="lum_agn(ergs/s)"): lpl=float(data[3])
			elif (data[2]=="agn_power_law_index"): alpha=float(data[3])
			elif (data[2]=="rstar(cm)"): 
				rbb=float(data[3])
				disk_radmin=float(data[3])
			elif (data[2]=="tstar"): tbb=float(data[3])
			elif (data[2]=="Star_radiation(y=1)"): istar=int(data[3])
			elif (data[2]=="Disk_radiation(y=1)"): idisk=int(data[3])
			elif (data[2]=="QSO_BH_radiation(y=1)"): ibh=int(data[3])
			elif (data[2]=="disk.mdot(msol/yr)"): disk_mdot=float(data[3])
			elif (data[2]=="disk.radmax(cm)"): disk_radmax=float(data[3])
			elif (data[2]=="mstar(msol)"): mbh=float(data[3])		
			elif (data[2]=="no_observers"): nobs=int(data[3])
			elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
			elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
			elif (data[1]=="Freq."):
				titles[0:len(line)-2]=data[1:len(line)-1]
		else:
			data=line.split()
			freq.append(data[0])
			wavelength.append(data[1])
			emitted.append(data[2])
			star_bl.append(data[3])
			disk.append(data[4])
			wind.append(data[5])
			hitsurf.append(data[6])
			scattered.append(data[7])
			tempspec.append(data[8:len(data)])
			for i in range(nobs):   			
				if (float(data[8+i])>fmax[i]): fmax[i]=float(data[8+i])
    				if (float(data[8+i])<fmin[i]): fmin[i]=float(data[8+i])


if (len(sys.argv)>3):
	lmin=float(sys.argv[3])
	lmax=float(sys.argv[4])








bin=float(ibin)
smoothtempspec=[]


for i in range(len(tempspec)-ibin):
	temp1=[]
	for j in range(nobs):
		temp=0.0
		for k in range(ibin):
			temp=temp+float(tempspec[i+k][j])
		temp1.append(temp/bin)
	smoothtempspec.append(temp1)


spec=np.transpose(tempspec)
smoothspec=np.transpose(smoothtempspec)

ny=nobs/2


fig=plt.figure(figsize=(8.3,11.7),dpi=80)
fig.suptitle(fname,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=8

#	ax.axis([wavelength[len(wavelength)-1],wavelength[0],0,fmax])




for i in range(nobs):
	ax=fig.add_subplot(ny+1,2,i+1)
	plt.xlim(lmin,lmax)
	ax.set_title(titles[8+i],fontsize=14)
	ax.plot(wavelength[0:-ibin],smoothspec[i])
	ax.axvline(x=1550)
        plt.text(1550,fmin[i],'CIV',fontsize=6)
	ax.axvline(x=1032)
	ax.axvline(x=1038)
        plt.text(1038,fmin[i],'OVI',fontsize=6)	
	ax.axvline(x=1239)
	ax.axvline(x=1243)
        plt.text(1243,fmin[i],'NV',fontsize=6)
	ax.axvline(x=1394)
	ax.axvline(x=1403)
        plt.text(1403,fmin[i],'SiIV',fontsize=6)


plt.savefig(sys.argv[1]+'spectrum_summary.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')



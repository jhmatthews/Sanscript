#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 
import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np
import subroutines as subrtn
#import matplotlib as mpl
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['font.family'] = 'serif'


titles=[]
freq=[]
wavelength=[]

t_Emitted=[]
t_CenSrc=[]
t_Disk=[]
t_Wind=[]
t_HitSurf=[]
t_Scattered=[]

Emitted=[]
CenSrc=[]
Disk=[]
Wind=[]
HitSurf=[]
Scattered=[]


titles2=[]
freq2=[]
wavelength2=[]

t_Emitted2=[]
t_CenSrc2=[]
t_Disk2=[]
t_Wind2=[]
t_HitSurf2=[]
t_Scattered2=[]

Emitted2=[]
CenSrc2=[]
Disk2=[]
Wind2=[]
HitSurf2=[]
Scattered2=[]

tempspec=[]
tempspec2=[]
i=-1
fmax=[0,0,0,0,0,0,0,0,0,0,0]
fmin=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]
fmax2=[0,0,0,0,0,0,0,0,0,0,0]
fmin2=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]
normalised=False


if (len(sys.argv)<3):
	ibin=1
else:
	ibin=int(sys.argv[3])


#first open file 1
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
			elif (data[2]=="no_observers"): print 'nobs'
			elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
			elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
			elif (data[1]=="Freq."):
				titles[0:len(line)-2]=data[1:len(line)-1]
		else:
			data=line.split()
			freq.append(data[0])
			wavelength.append(data[1])
			t_Emitted.append(data[2])
			t_CenSrc.append(data[3])
			t_Disk.append(data[4])
			t_Wind.append(data[5])
			t_HitSurf.append(data[6])
			t_Scattered.append(data[7])
			tempspec.append(data[8:len(data)])
			for i in range(nobs):   			
				if (float(data[8+i])>fmax[i]): fmax[i]=float(data[8+i])
    				if (float(data[8+i])<fmin[i]): fmin[i]=float(data[8+i])



#now open file 2!
fname2=sys.argv[2]+".spec"
print fname2
inp =open(fname2,'r')
for line in inp.readlines():
	if (len(line)>4):
		if (line[0]=='#'):
			data=line.split()
			print data[2]
			if (data[2]=="lum_agn(ergs/s)"): lpl2=float(data[3])
			elif (data[2]=="agn_power_law_index"): alpha2=float(data[3])
			elif (data[2]=="rstar(cm)"): 
				rbb2=float(data[3])
				disk_radmin2=float(data[3])
			elif (data[2]=="tstar"): tbb2=float(data[3])
			elif (data[2]=="Star_radiation(y=1)"): ista2r=int(data[3])
			elif (data[2]=="Disk_radiation(y=1)"): idisk2=int(data[3])
			elif (data[2]=="QSO_BH_radiation(y=1)"): ibh2=int(data[3])
			elif (data[2]=="disk.mdot(msol/yr)"): disk_mdot2=float(data[3])
			elif (data[2]=="disk.radmax(cm)"): disk_radmax2=float(data[3])
			elif (data[2]=="mstar(msol)"): mbh2=float(data[3])		
			elif (data[2]=="no_observers"): nobs2=int(data[3])
			elif (data[2]=="no_observers"): print 'nobs'
			elif (data[2]=="spectrum_wavemin"): lmin2=float(data[3])		
			elif (data[2]=="spectrum_wavemax"): lmax2=float(data[3])
			elif (data[1]=="Freq."):
				titles2[0:len(line)-2]=data[1:len(line)-1]
		else:
			data=line.split()
			freq2.append(data[0])
			wavelength2.append(data[1])
			t_Emitted2.append(data[2])
			t_CenSrc2.append(data[3])
			t_Disk2.append(data[4])
			t_Wind2.append(data[5])
			t_HitSurf2.append(data[6])
			t_Scattered2.append(data[7])
			tempspec2.append(data[8:len(data)])
			for i in range(nobs):   			
				if (float(data[8+i])>fmax2[i]): fmax2[i]=float(data[8+i])
    				if (float(data[8+i])<fmin2[i]): fmin2[i]=float(data[8+i])










if (len(sys.argv)==6):
	lmin=float(sys.argv[4])
	lmax=float(sys.argv[5])
	#print lmin, lmax




bin=float(ibin)
smoothtempspec=[]
sum_smooth=0.0

for i in range(len(tempspec)-ibin):
	temp1=[]
	for j in range(nobs):
		temp=0.0
		t1=t2=t3=t4=t5=t6=0.0
		for k in range(ibin):
			temp=temp+float(tempspec[i+k][j])
			t1=t1+float(t_Emitted[i+k])
			t2=t2+float(t_CenSrc[i+k])
			t3=t3+float(t_Disk[i+k])
			t4=t4+float(t_Wind[i+k])
			t5=t5+float(t_HitSurf[i+k])
			t6=t6+float(t_Scattered[i+k])
		temp1.append(temp/bin)
		t1=t1/bin
		t2=t2/bin
		t3=t3/bin
		t4=t4/bin
		t5=t5/bin
		t6=t6/bin
	smoothtempspec.append(temp1)
	#sum_smooth=sum_smooth+temp1
	Emitted.append(t1)
	CenSrc.append(t2)
	Disk.append(t3)
	Wind.append(t4)
	HitSurf.append(t5)
	Scattered.append(t6)

spec=np.transpose(tempspec)
smoothspec=np.transpose(smoothtempspec)


smoothtempspec2=[]
sum_smooth2=0.0
for i in range(len(tempspec2)-ibin):
	temp12=[]
	for j in range(nobs2):
		temp2=0.0
		t12=t22=t32=t42=t52=t62=0.0
		for k in range(ibin):
			temp2=temp2+float(tempspec2[i+k][j])
			t12=t12+float(t_Emitted2[i+k])
			t22=t22+float(t_CenSrc2[i+k])
			t32=t32+float(t_Disk2[i+k])
			t42=t42+float(t_Wind2[i+k])
			t52=t52+float(t_HitSurf2[i+k])
			t62=t62+float(t_Scattered2[i+k])
		temp12.append(temp2/bin)
		t12=t12/bin
		t22=t22/bin
		t32=t32/bin
		t42=t42/bin
		t52=t52/bin
		t62=t62/bin
	smoothtempspec2.append(temp12)
	#sum_smooth=sum_smooth+temp1
	Emitted2.append(t1)
	CenSrc2.append(t2)
	Disk2.append(t3)
	Wind2.append(t4)
	HitSurf2.append(t5)
	Scattered2.append(t6)

spec2=np.transpose(tempspec2)
smoothspec2=np.transpose(smoothtempspec2)




for i in range(len(smoothspec)):
	print i, len(smoothspec[i])
	for j in range(len(smoothspec[i])):
		smoothspec[i][j]=(smoothspec[i][j]-smoothspec2[i][j])






ny=nobs/2

#set some parameters for figures
fig=plt.figure(figsize=(8.3,11.7),dpi=80)
fig.suptitle(fname,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=10

#	ax.axis([wavelength[len(wavelength)-1],wavelength[0],0,fmax])



#print lmin, lmax
for i in range(nobs):
		#create spectrum summary figure, with absorption line locations overlaid
	ax=fig.add_subplot(ny+1,2,i+1)
	ax.set_title(titles[8+i],fontsize=14)
	ax.plot(wavelength[0:-ibin],smoothspec[i], c='k')
	ax.axvline(x=1550, c='r')
        plt.text(1550,fmin[i],'CIV',fontsize=6)
	ax.axvline(x=1032, c='b')
	ax.axvline(x=1038, c='b')
        plt.text(1038,fmin[i],'OVI',fontsize=6)	
	ax.axvline(x=1239, c='g')
	ax.axvline(x=1243, c='g')
        plt.text(1243,fmin[i],'NV',fontsize=6)
	ax.axvline(x=1394, c='c')
	ax.axvline(x=1403, c='c')
        plt.text(1403,fmin[i],'SiIV',fontsize=6)
	ax.axvline(x=1026, c='y')
	ax.axvline(x=1215, c='y')
        plt.text(1403,fmin[i],'Ly',fontsize=6)

		#ensure that the x axis is scaled within limits specified.
	locator=ax.yaxis.get_major_locator()
	ax.set_autoscale_on(False)
	ax.set_xlim(lmin,lmax)
	locator=ax.yaxis.get_major_locator()
	ax.set_ylim(locator.autoscale())

if (len(sys.argv)>4): 
	#save spectrum summary figure with range given
	plt.savefig(sys.argv[1]+"_range"+sys.argv[3]+"_"+sys.argv[4]+'res_summary.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

else:
	#save spectrum summary figure
	plt.savefig(sys.argv[1]+'res_summary.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')


fig=plt.figure(figsize=(8.3,11.7),dpi=80)
fig.suptitle(fname,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=8

#	ax.axis([wavelength[len(wavelength)-1],wavelength[0],0,fmax])



for i in range(len(Emitted)):
	Emitted[i]=Emitted[i]-Emitted2[i]
	CenSrc[i]=CenSrc[i]-CenSrc2[i]
	Disk[i]=Disk[i]-Disk2[i]
	Wind[i]=Wind[i]-Wind2[i]
	HitSurf[i]=HitSurf[i]-HitSurf2[i]
	Scattered[i]=Scattered[i]-Scattered2[i]


ax=fig.add_subplot(3,2,1)
plt.xlim(lmin,lmax)
ax.set_title("Emitted",fontsize=14)
ax.plot(wavelength[0:-ibin],Emitted,label="Emitted")
ax.plot(wavelength[0:-ibin],CenSrc,label="CenSrc")
ax.plot(wavelength[0:-ibin],Disk,label="Disk")
ax.plot(wavelength[0:-ibin],Wind,label="Wind")
ax.plot(wavelength[0:-ibin],HitSurf,label="HitSurf")
ax.plot(wavelength[0:-ibin],Scattered,label="Scattered")
ax.legend()
ax=fig.add_subplot(3,2,2)
plt.xlim(lmin,lmax)
ax.set_title("CenSrc",fontsize=14)
ax.plot(wavelength[0:-ibin],CenSrc)
ax=fig.add_subplot(3,2,3)
plt.xlim(lmin,lmax)
ax.set_title("Disk",fontsize=14)
ax.plot(wavelength[0:-ibin],Disk)
ax=fig.add_subplot(3,2,4)
plt.xlim(lmin,lmax)
ax.set_title("Wind",fontsize=14)
ax.plot(wavelength[0:-ibin],Wind)
ax=fig.add_subplot(3,2,5)
plt.xlim(lmin,lmax)
ax.set_title("HitSurf",fontsize=14)
ax.plot(wavelength[0:-ibin],HitSurf)
ax=fig.add_subplot(3,2,6)
plt.xlim(lmin,lmax)
ax.set_title("Scattered",fontsize=14)
ax.plot(wavelength[0:-ibin],Scattered)





if (len(sys.argv)>4):
		#save spectrum sources figure with range given	
	plt.savefig(sys.argv[1]+"_range"+sys.argv[3]+"_"+sys.argv[4]+'res_sources.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

else:
		#save spectrum sources figure
	plt.savefig(sys.argv[1]+'res_sources.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

yno=str(raw_input('do you want to write to file y/n?'))
orig_filename=sys.argv[1]
if yno=='y':
	for i in range(nobs):
		filename=orig_filename+'_fileoutput'+str(i+1)
		subrtn.write_files(wavelength[0:-ibin], smoothspec[i], filename)













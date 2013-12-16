#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 

#--------------------------------------------------------
# This is intended as a general python script where options are specified via arguments
#
#JM
#----------------------------------------------------------


import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np
import subroutines as subrtn
import functions as fn
from raw_str import raw
import workhorse as wh
from constants import *
#import matplotlib as mpl

#wh.setpars()

#-------------------------------------------------------------------------------
#Set Booleans
#we have an array of Booleans

print 'Hi there, let\'s make some plots'

no_obs=True
format='jpg'
mode=wh.modeclass(False, False, False, False, False, False, False, False,False, True, False)
store=wh.stored_args(0,0,0,0,0,0,0)

#read system arguments and set modes. set values to store.
wh.read_args(sys.argv, mode, store)



#-------------------------------------------------------------------------------
# IF IN SUPERMONGO MODE
if mode.sm:
	format='jpg'


	fname_read=False
	which_to_plot=[]
	labels_to_plot=[]
	inp_cmd =open(fname_cmd,'r')
	print 'INPUTS:\n'
	for line in inp_cmd.readlines():
		data=line.split()
		if len(data)>1:
			print data[0], data[1]
			if data[0]=='fname': 
				fname=str(data[1])+'.spec'
				savename=str(data[1])
				fname_read=True
				main_title=fname
			if data[0]=='lmin': lmin=float(data[1])
			if data[0]=='lmax': lmax=float(data[1])
			if data[0]=='norm': 
				if data[1]==1: normalised=True
			if data[0]=='plot': which_to_plot.append(int(data[1]))
			if data[0]=='label': labels_to_plot.append(data[1])
			if data[0]=='title': main_title=data[1]
			if data[0]=='xlabel': xlab=data[1]
			if data[0]=='ylabel': ylab=data[1]
			if data[0]=='rcparamstr': plt.rcParams[data[1]] = data[2]
			if data[0]=='rcparamint': plt.rcParams[data[1]] = int(data[2])
			if data[0]=='rcparamfl': plt.rcParams[data[1]] = float(data[2])
	
			if data[0]=='store.ibin': store.ibin=int(data[1])
			if data[0]=='format': format=data[1]

	if fname_read:
		inp =open(fname,'r')
	else: 
		if 'spec' in sys.argv[1]:
			fname=sys.argv[1]
		else:
			fname=sys.argv[1]+".spec"
		savename=sys.argv[1]
		inp =open(fname,'r')

if mode.comp or mode.resid:
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	if 'spec' in sys.argv[2]:
		fname2=sys.argv[2]
	else:
		fname2=sys.argv[2]+".spec"
		
	store.ibin=int(sys.argv[3])
	print fname, ' compared against ', fname2
else:
	#first open file 1
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	store.ibin=int(sys.argv[2])
	print fname




#Initialise arrays -----------------------------------------------------------------------
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

#------------------------------------------------------------------------------
# Arrays initialised, read in data
print 'reading data from .spec_tot file.'

inp =open(fname,'r')
for line in inp.readlines():
	if (len(line)>4):
		if (line[0]=='#'):
			data=line.split()
			#print data[2]
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
			elif (data[2]=="no_observers"): no_obs=False
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
			if no_obs:
				nobs=int(raw_input('No observers?? How many!??:'))
				no_obs=False

#if you are in comparison or residual mode, open file 2!--------------------------

if mode.comp or mode.resid:
	no_obs=True
	print 'reading data from comparison .spec file.'
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
				elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
				elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
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
				if no_obs: 
					nobs2=nobs
					no_obs=False

#-------------------------------------------------------------------------------------

if mode.range:
	lmin=store.lmin_arg
	lmax=store.lmax_arg
	print 'you are plotting in range ', lmin, lmax

#Smooth spectrum.
print 'smoothing spectrum.'
bin=float(store.ibin)
print 'smoothing factor is ', bin
smoothtempspec=[]
sum_smooth=0.0

for i in range(len(t_Emitted)-store.ibin):
	temp1=[]
	for j in range(nobs):
		temp=0.0
		t1=t2=t3=t4=t5=t6=0.0
		for k in range(store.ibin):
			t1=t1+float(t_Emitted[i+k])
			t2=t2+float(t_CenSrc[i+k])
			t3=t3+float(t_Disk[i+k])
			t4=t4+float(t_Wind[i+k])
			t5=t5+float(t_HitSurf[i+k])
			t6=t6+float(t_Scattered[i+k])
		t1=t1/bin
		t2=t2/bin
		t3=t3/bin
		t4=t4/bin
		t5=t5/bin
		t6=t6/bin
	Emitted.append(t1)
	CenSrc.append(t2)
	Disk.append(t3)
	Wind.append(t4)
	HitSurf.append(t5)
	Scattered.append(t6)

for i in range(len(t_Emitted)-store.ibin):
	for j in range(nobs2):
		t12=t22=t32=t42=t52=t62=0.0
		for k in range(store.ibin):
			t12=t12+float(t_Emitted2[i+k])
			t22=t22+float(t_CenSrc2[i+k])
			t32=t32+float(t_Disk2[i+k])
			t42=t42+float(t_Wind2[i+k])
			t52=t52+float(t_HitSurf2[i+k])
			t62=t62+float(t_Scattered2[i+k])
		t12=t12/bin
		t22=t22/bin
		t32=t32/bin
		t42=t42/bin
		t52=t52/bin
		t62=t62/bin
	Emitted2.append(t12)
	CenSrc2.append(t22)
	Disk2.append(t32)
	Wind2.append(t42)
	HitSurf2.append(t52)
	Scattered2.append(t62)

save_suffix='spectot'

#for i in range(len(CenSrc)-1):
#	if i<len(CenSrc)-1: delta_lambda=(1.0e-8)*np.fabs(float(wavelength[i])-float(wavelength[i+1]))
#	CenSrc[i]=CenSrc[i]/delta_lambda
#	Disk[i]=Disk[i]/delta_lambda
#	Emitted[i]=Emitted[i]/delta_lambda

#for i in range(len(CenSrc2)-1):
#	if i<len(CenSrc2)-1: delta_lambda=(1.0e-8)*np.fabs(float(wavelength2[i])-float(wavelength2[i+1]))
#	Emitted2[i]=Emitted2[i]/delta_lambda
#	Disk2[i]=Disk2[i]/delta_lambda
#	CenSrc2[i]=CenSrc2[i]/delta_lambda

planck2=[]
i=0
rj=[]
rjb=[]
for lambstr in wavelength[0:-store.ibin]:
	#print wavelength[i]
	if i<len(CenSrc)-1: delta_lambda=(1.0e-8)*np.fabs(float(wavelength[i])-float(wavelength[i+1]))
	lamb=float(lambstr)*1.0e-8   #lambda in cm
	tenpc=100.0*3.086E18
	rstar=3.828e11
	#correct=4.0*PI*PI*(rstar**2)
	correct=PI*(rstar**2)/(tenpc**2)
	I=(fn.planck_lambda(23738.0, lamb))*correct*1.0e-8
	II=fn.RJ(23738.0, lamb)*correct*1.0e-8
	planck2.append(I)
	rj.append(II)
	i+=1
#planck=[planck_func(23738.0, 3.0E10/(lamb*1.0E8)) for lamb in wavelength]
planck=np.array(planck2)
planck2b=[]
i=0
for lambstr in wavelength2[0:-store.ibin]:
	#print wavelength[i]
	if i<len(CenSrc)-1: delta_lambda=(1.0e-8)*np.fabs(float(wavelength2[i])-float(wavelength2[i+1]))
	lamb=float(lambstr)*1.0e-8   #lambda in cm
	tenpc=100.0*3.086E18
	rstar=3.828e11
	#correct=4.0*PI*PI*(rstar**2)
	correct=PI*(rstar**2)/(tenpc**2)
	I=(fn.planck_lambda(23738.0, lamb))*correct*1.0e-8
	II=fn.RJ(23738.0, lamb)*correct*1.0e-8
	planck2b.append(I)
	rjb.append(II)
	i+=1
#planck=[planck_func(23738.0, 3.0E10/(lamb*1.0E8)) for lamb in wavelength]
planckb=np.array(planck2b)

#------------------------------------------------------------------------------------
print lmin, lmax
#lmin=1000
#lmax=100000	
#Sources plot
if mode.sources:
	print 'Plotting sources.'
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	#plt.xlim(lmin,lmax)
	fig.suptitle(fname,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=8




	if mode.resid:
		for i in range(len(Emitted)):
			Emitted[i]=Emitted[i]-Emitted2[i]
			CenSrc[i]=CenSrc[i]-CenSrc2[i]
			Disk[i]=Disk[i]-Disk2[i]
			#Wind[i]=Wind[i]-Wind2[i]
			#HitSurf[i]=HitSurf[i]-HitSurf2[i]
			#Scattered[i]=Scattered[i]-Scattered2[i]


	ax=fig.add_subplot(3,2,1)
	plt.xlim(lmin,lmax)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	plt.xlim(lmin,lmax)
	ax.set_title("Emitted_"+fname,fontsize=14)
	ax.plot(wavelength[0:-store.ibin],Emitted,label="Emitted")
	ax.plot(wavelength[0:-store.ibin],CenSrc,label="CenSrc")
	ax.plot(wavelength[0:-store.ibin],Disk,label="Disk")
	ax.plot(wavelength[0:-store.ibin],Wind,label="Wind")
	ax.plot(wavelength[0:-store.ibin],HitSurf,label="HitSurf")
	#ax.plot(wavelength[0:-store.ibin],Scattered,label="Scattered")
	ax.legend(loc=2)
	#plt.xlim(1.0e4,lmax)
	#plt.ylim(1.0e-15,1.0e-9)
	ax=fig.add_subplot(3,2,2)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	if mode.comp:
		#plt.text(0.5*(float(lmin+lmax)),2,fname,fontsize=6)
		ax.set_title("Emitted_"+fname2,fontsize=14)
		ax.plot(wavelength2[0:-store.ibin],Emitted2,label="Emitted")
		ax.plot(wavelength2[0:-store.ibin],CenSrc2,label="CenSrc")
		ax.plot(wavelength2[0:-store.ibin],Disk2,label="Disk")
		ax.plot(wavelength2[0:-store.ibin],Wind2,label="Wind")
		ax.plot(wavelength2[0:-store.ibin],HitSurf2,label="HitSurf")
		#ax.plot(wavelength2[0:-store.ibin],Scattered2,label="Scattered")
		ax.legend(loc=2)
	plt.xlim(lmin,lmax)
	#plt.ylim(1.0e-15,1.0e-9)
	ax=fig.add_subplot(3,2,3)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	ax.set_title("CenSrc",fontsize=14)
	ax.plot(wavelength[0:-store.ibin],CenSrc, c='g')
	if mode.comp: 
		ax.plot(wavelength2[0:-store.ibin],CenSrc2, c='b')
		plt.rcParams['text.color']='green'
		plt.text(0.5*(float(lmin+lmax)),2.0e33,fname,fontsize=10)
		plt.rcParams['text.color']='blue'
		plt.text(0.5*(float(lmin+lmax)),3.0e33,fname2,fontsize=10)
		plt.rcParams['text.color']='black'
		#ax.plot(wavelength[0:-store.ibin],planck, c='r')
		#ax.plot(wavelength[0:-store.ibin],rj, c='m')
	plt.xlim(lmin,lmax)
	ax=fig.add_subplot(3,2,4)
	if mode.log: ax.set_xscale('log')
	if mode.log: ax.set_yscale('log')
	ax.set_title("Disk",fontsize=14)
	ax.plot(wavelength[0:-store.ibin],Disk, c='g')
	if mode.comp: ax.plot(wavelength2[0:-store.ibin],Disk2, c='b')
	plt.xlim(lmin,lmax)
	ax=fig.add_subplot(3,2,6)
	#if mode.log: ax.set_xscale('log')
	#if mode.log: ax.set_yscale('log')
	ax.set_title("Wind",fontsize=14)
	plt.xlim(lmin,lmax)
	ax.plot(wavelength[0:-store.ibin],np.array(Wind), c='g')
	if mode.comp: ax.plot(wavelength[0:-store.ibin],Wind2, c='b')
	plt.xlim(lmin,lmax)
	ax=fig.add_subplot(3,2,5)
	#if mode.log: ax.set_xscale('log')
	#if mode.log: ax.set_yscale('log')
	ax.set_title("Scattered",fontsize=14)
	print np.array(CenSrc2)/np.array(CenSrc)
	#for i in range(len(CenSrc)):
		#print 1.0*CenSrc[i]/CenSrc2[i], i, wavelength[i]
		
	ax.plot(wavelength[0:-store.ibin],np.array(Scattered), c='g')
	plt.xlim(lmin,lmax)
	if mode.comp: ax.plot(wavelength[0:-store.ibin],Scattered2, c='b')
	x=0.5	
	plt.text(0,0,"i am a %f"%x)

        plt.xlim(lmin,lmax)
	if mode.range:
			#save spectrum sources figure with range given	
		savename=sys.argv[1]+"_range"+str(store.lmin_arg)+"_"+str(store.lmax_arg)+'_'+save_suffix+'sources.jpg'
		plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

	else:
			#save spectrum sources figure
		savename=sys.argv[1]+'_'+save_suffix+'sources.jpg'
		plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

	yno=str(raw_input('do you want to write to file y/n?'))
	orig_filename=sys.argv[1]
	if yno=='y':
		for i in range(nobs):
			filename=orig_filename+'_fileoutput'+str(i+1)
			subrtn.write_files(wavelength[0:-store.ibin], smoothspec[i], filename)

os.system('open -a preview '+savename)

#ALL DONE
#-------------------------------------------------------------------------------









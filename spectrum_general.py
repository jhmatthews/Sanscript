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
from raw_str import raw
#import matplotlib as mpl

#set any matplotlib parameters
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.family'] = 'serif'

#-------------------------------------------------------------------------------
#Set Booleans
format='jpg'
sm_mode=False
norm_mode=False
res_mode=False
comp_mode=False
Relative=False
vlines=True
range_mode=False
Sources=False
no_obs=True

# help message
def help_me():
	help_string=''' You want help...ok...
		        usage genplot filename [ibin] [-n] [-s sm_commands] [-r lmin lmax] [-c] [nolines] [sources]
 		        -n means normalised
			-s means SM mode (you 
			-r means specify lmin and lmax
			-c means comparison mode
			-res means residual mode
			-rel means relative residuals
			nolines means no lines
			sources means also plot sources for spectra e.g. CenSrc, Emitted.
			This program will now exit.\n
			'''
	print help_string
	sys.exit()
	return 0


#read arguments from command line.

if (len(sys.argv)<3):
		ibin=1


for i in range(len(sys.argv)):
	if sys.argv[i]=='-s': 
		sm_mode=True
		fname_cmd=sys.argv[i+1]
	if sys.argv[i]=='-n': norm_mode=True
	if sys.argv[i]=='-r': 
		range_mode=True
		lmin_arg=float(sys.argv[i+1])
		lmax_arg=float(sys.argv[i+2])
	if sys.argv[i]=='-c': 
		comp_mode=True
		print 'comp'
	if sys.argv[i]=='-nc': 
		norm_mode=True
		comp_mode=True	
	if sys.argv[i]=='-res': res_mode=True
	if sys.argv[i]=='h': dummy=help_me()
	if sys.argv[i]=='-rel': 
		res_mode=True
		Relative=True
	if sys.argv[i]=='nolines': vlines=False
	if sys.argv[i]=='sources': Sources=True


#-------------------------------------------------------------------------------
# IF IN SUPERMONGO MODE
if sm_mode:
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
	
			if data[0]=='ibin': ibin=int(data[1])
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

if comp_mode or res_mode:
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	if 'spec' in sys.argv[2]:
		fname2=sys.argv[2]
	else:
		fname2=sys.argv[2]+".spec"
		
	ibin=int(sys.argv[3])
	print fname, ' compared against ', fname2
else:
	#first open file 1
	if 'spec' in sys.argv[1]:
		fname=sys.argv[1]
	else:
		fname=sys.argv[1]+".spec"
	ibin=int(sys.argv[2])
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
print 'reading data from .spec file.'

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
			for i in range(nobs):   			
				if (float(data[8+i])>fmax[i]): fmax[i]=float(data[8+i])
    				if (float(data[8+i])<fmin[i]): fmin[i]=float(data[8+i])



#if you are in comparison or residual mode, open file 2!--------------------------

if comp_mode or res_mode:
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
				for i in range(nobs2):   			
					if (float(data[8+i])>fmax2[i]): fmax2[i]=float(data[8+i])
	    				if (float(data[8+i])<fmin2[i]): fmin2[i]=float(data[8+i])




#-------------------------------------------------------------------------------------

#Smooth spectrum.
print 'smoothing spectrum.'
bin=float(ibin)
smoothtempspec=[]
sum_smooth=0.0
if range_mode:
	lmin=lmin_arg
	lmax=lmax_arg

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
	Emitted2.append(t12)
	CenSrc2.append(t22)
	Disk2.append(t32)
	Wind2.append(t42)
	HitSurf2.append(t52)
	Scattered2.append(t62)

spec2=np.transpose(tempspec2)
smoothspec2=np.transpose(smoothtempspec2)

#-------------------------------------------------------------------------------------

if norm_mode:
	delta_norm=1
	print 'normalising spectra.'
	for i in range(nobs):
		#normalisation_flux=sum(smoothspec[i])/len(smoothspec[i])
		smoothspec[i]=subrtn.normalise(smoothspec[i], delta_norm)
		if comp_mode or res_mode: smoothspec2[i]=subrtn.normalise(smoothspec2[i], delta_norm)


if res_mode:
	if Relative: print 'we are doing relative residuals'
	for i in range(len(smoothspec)):
		print i, len(smoothspec[i])
		for j in range(len(smoothspec[i])):
			if Relative: 
				orig=smoothspec[i][j]
				smoothspec[i][j]=(smoothspec[i][j]-smoothspec2[i][j])/orig
			else:
				smoothspec[i][j]=(smoothspec[i][j]-smoothspec2[i][j])


#-------------------------------------------------------------------------------------

if sm_mode:
	#set some parameters for figures
	fig=plt.figure(figsize=(8.3,11.7),dpi=160)
	if main_title!='notitle': fig.suptitle(main_title,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=10

	#	ax.axis([wavelength[len(wavelength)-1],wavelength[0],0,fmax])


	if len(which_to_plot)==0:
		which_to_plot=[a for a in range(nobs)]

	ny=len(which_to_plot+1)/2

	i_cnt=0
	#print lmin, lmax
	print 'plotting...'
	for i in which_to_plot:
		i_cnt=i_cnt+1
			#create spectrum summary figure, with absorption line locations overlaid
		ax=fig.add_subplot(ny,1,i_cnt)
		#ax.tick_params(axis='both', which='major', labelsize=10)
		plt.rcParams['text.usetex']='True'
		#plt.lines.set_markeredgecolor('0.1')
		#print plt.rcParams['lines.markeredgecolor']
		ax.set_title(raw(labels_to_plot[i_cnt-1]),fontsize=18)
		ax.plot(wavelength[0:-ibin],smoothspec[i], c='b')
		if comp_mode: ax.plot(wavelength[0:-ibin],smoothspec2[i], c='0.2', linestyle='--')
		ax.set_ylabel(raw('{\rm '+ylab+'}'), fontsize=14)
		ax.set_xlabel(raw(xlab), fontsize=14)
		if vlines:
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

	if range_mode: 
		#save spectrum summary figure with range given
		savename=savename+"_range"+str(lmin)+"_"+str(lmax)+'spectrum_sm.'+format
		plt.savefig(savename,dpi=160,facecolor='w',edgecolor='w',orientation='portrait')

	else:
		#save spectrum summary figure
		savename=savename+'spectrum_sm.'+format
		plt.savefig(savename,dpi=160,facecolor='w',edgecolor='w',orientation='portrait')
else:
	ny=(nobs+1)/2
	main_title=str(raw_input('Enter a title'))
	#set some parameters for figures
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	fig.suptitle(main_title,fontsize=18,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=10


	#print lmin, lmax
	for i in range(nobs):
			#create spectrum summary figure, with absorption line locations overlaid
		ax=fig.add_subplot(ny,2,i+1)
		ax.set_title(titles[8+i],fontsize=14)
		ax.plot(wavelength[0:-ibin],smoothspec[i], c='g')
		if comp_mode: ax.plot(wavelength[0:-ibin],smoothspec2[i], c='b')
		if vlines:
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


	#save files.
	save_suffix=''
	if comp_mode: save_suffix='comp'
	if res_mode: save_suffix='res'
	if sm_mode: save_suffix='sm'
	

	if range_mode: 
		print 'range mode'
		#save spectrum summary figure with range given
		savename=sys.argv[1]+"_range"+str(lmin)+"_"+str(lmax)+'_'+save_suffix+'summary.'+format
		plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

	else:
		#save spectrum summary figure
		savename=sys.argv[1]+'_'+save_suffix+'summary.'+format
		plt.savefig(savename,dpi=80,facecolor='w',edgecolor='w',orientation='portrait') 





#-------------------------------------------------------------------------------
#Sources plot
if Sources:
	print 'also plotting sources.'
	fig=plt.figure(figsize=(8.3,11.7),dpi=80)
	fig.suptitle(fname,fontsize=24,fontweight='bold')
	fig.subplots_adjust(hspace=0.3,wspace=0.2)
	plt.rcParams['font.size']=8




	if res_mode:
		for i in range(len(Emitted)):
			Emitted[i]=Emitted[i]-Emitted2[i]
			CenSrc[i]=CenSrc[i]-CenSrc2[i]
			Disk[i]=Disk[i]-Disk2[i]
			Wind[i]=Wind[i]-Wind2[i]
			HitSurf[i]=HitSurf[i]-HitSurf2[i]
			Scattered[i]=Scattered[i]-Scattered2[i]


	ax=fig.add_subplot(3,2,1)
	plt.xlim(lmin,lmax)
	ax.set_title("Emitted_"+fname,fontsize=14)
	ax.plot(wavelength[0:-ibin],Emitted,label="Emitted")
	ax.plot(wavelength[0:-ibin],CenSrc,label="CenSrc")
	ax.plot(wavelength[0:-ibin],Disk,label="Disk")
	ax.plot(wavelength[0:-ibin],Wind,label="Wind")
	ax.plot(wavelength[0:-ibin],HitSurf,label="HitSurf")
	ax.plot(wavelength[0:-ibin],Scattered,label="Scattered")
	ax.legend()
	ax=fig.add_subplot(3,2,2)
	if comp_mode:
		plt.xlim(lmin,lmax)
		#plt.text(0.5*(float(lmin+lmax)),2,fname,fontsize=6)
		ax.set_title("Emitted_"+fname2,fontsize=14)
		ax.plot(wavelength[0:-ibin],Emitted2,label="Emitted")
		ax.plot(wavelength[0:-ibin],CenSrc2,label="CenSrc")
		ax.plot(wavelength[0:-ibin],Disk2,label="Disk")
		ax.plot(wavelength[0:-ibin],Wind2,label="Wind")
		ax.plot(wavelength[0:-ibin],HitSurf2,label="HitSurf")
		ax.plot(wavelength[0:-ibin],Scattered2,label="Scattered")
		ax.legend(loc=2)

	ax=fig.add_subplot(3,2,3)
	plt.xlim(lmin,lmax)
	ax.set_title("CenSrc",fontsize=14)
	ax.plot(wavelength[0:-ibin],CenSrc, c='g')
	if comp_mode: 
		ax.plot(wavelength[0:-ibin],CenSrc2, c='b')
		plt.rcParams['text.color']='green'
		plt.text(0.5*(float(lmin+lmax)),2.0e-11,fname,fontsize=10)
		plt.rcParams['text.color']='blue'
		plt.text(0.5*(float(lmin+lmax)),3.0e-11,fname2,fontsize=10)
		plt.rcParams['text.color']='black'
	ax=fig.add_subplot(3,2,4)
	plt.xlim(lmin,lmax)
	ax.set_title("Disk",fontsize=14)
	ax.plot(wavelength[0:-ibin],Disk, c='g')
	if comp_mode: ax.plot(wavelength[0:-ibin],Disk2, c='b')
	ax=fig.add_subplot(3,2,5)
	plt.xlim(lmin,lmax)
	ax.set_title("Wind",fontsize=14)
	ax.plot(wavelength[0:-ibin],Wind, c='g')
	if comp_mode: ax.plot(wavelength[0:-ibin],Wind2, c='b')
	ax=fig.add_subplot(3,2,6)
	plt.xlim(lmin,lmax)
	ax.set_title("HitSurf",fontsize=14)
	ax.plot(wavelength[0:-ibin],HitSurf, c='g')
	if comp_mode: ax.plot(wavelength[0:-ibin],HitSurf2, c='b')




	if range_mode:
			#save spectrum sources figure with range given	
		plt.savefig(sys.argv[1]+"_range"+sys.argv[4]+"_"+sys.argv[5]+'_'+save_suffix+'sources.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

	else:
			#save spectrum sources figure
		plt.savefig(sys.argv[1]+'_'+save_suffix+'sources.jpg',dpi=80,facecolor='w',edgecolor='w',orientation='portrait')

	yno=str(raw_input('do you want to write to file y/n?'))
	orig_filename=sys.argv[1]
	if yno=='y':
		for i in range(nobs):
			filename=orig_filename+'_fileoutput'+str(i+1)
			subrtn.write_files(wavelength[0:-ibin], smoothspec[i], filename)

os.system('open -a preview '+savename)

#ALL DONE
#-------------------------------------------------------------------------------









#! /Library/Frameworks/EPD64.framework/Versions/Current/bin/python 
import csv, sys, os, array, warnings
import matplotlib.pyplot as plt
import numpy as np
import subroutines as subrtn
from raw_str import raw
#import matplotlib as mpl


#xtick.minor.size     : 2      # minor tick size in points
#xtick.major.pad      : 4      # distance to major tick label in points
#xtick.minor.pad      : 4      # distance to the minor tick label in points
#xtick.color          : k      # color of the tick labels
#xtick.labelsize      : medium # fontsize of the tick labels
#xtick.direction      : in     # direction: in or out

#ytick.major.size     : 4      # major tick size in points
#ytick.minor.size     : 2      # minor tick size in points
#ytick.major.pad      : 4      # distance to major tick label in points
#ytick.minor.pad      : 4      # distance to the minor tick label in points
#ytick.color          : k      # color of the tick labels
#ytick.labelsize      : medium # fontsize of the tick labels
#ytick.direction      : in     # direction: in or out
ylab=''
xlab=''
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


tempspec=[]
i=-1
fmax=[0,0,0,0,0,0,0,0,0,0,0]
fmin=[1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99,1e99]
normalised=False

format='jpg'



if (len(sys.argv)<3):
	ibin=1

fname_cmd=sys.argv[1]
fname_read=False
which_to_plot=[]
labels_to_plot=[]
inp_cmd =open(fname_cmd,'r')
print 'INPUTS:\n'
for line in inp_cmd.readlines():
	data=line.split()
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
	fname=sys.argv[2]+'.spec'
	savename=sys.argv[2]
	inp =open(fname,'r')


	

print '\nFILENAME: '
print fname


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
			elif (data[2]=="no_observers"): print 'nobs'
			elif (data[2]=="spectrum_wavemin"): lmin=float(data[3])		
			elif (data[2]=="spectrum_wavemax"): lmax=float(data[3])
			elif (data[1]=="Freq."):
				titles[0:len(line)-2]=data[1:len(line)-1]
		else:
			data=line.split()
			freq.append(data[0])
			wavelength.append(data[1])
			tempspec.append(data[8:len(data)])
			for i in range(nobs):   			
				if (float(data[8+i])>fmax[i]): fmax[i]=float(data[8+i])
    				if (float(data[8+i])<fmin[i]): fmin[i]=float(data[8+i])


if (len(sys.argv)==5):
	lmin=float(sys.argv[3])
	lmax=float(sys.argv[4])


if (len(sys.argv)==4):
	normalised=True
	delta_norm=float(sys.argv[3])

if (len(sys.argv)==6):
	lmin=float(sys.argv[3])
	lmax=float(sys.argv[4])
	delta_norm=float(sys.argv[5])
	normalised=True



bin=float(ibin)
smoothtempspec=[]
sum_smooth=0.0

	
print 'binning...'
for i in range(len(tempspec)-ibin):
	temp1=[]
	for j in range(nobs):
		temp=0.0
		t1=t2=t3=t4=t5=t6=0.0
		for k in range(ibin):
			temp=temp+float(tempspec[i+k][j])
		temp1.append(temp/bin)
	smoothtempspec.append(temp1)
	#sum_smooth=sum_smooth+temp1


spec=np.transpose(tempspec)
smoothspec=np.transpose(smoothtempspec)


if normalised:
	print 'normalising...'
	for i in range(nobs):
		#normalisation_flux=sum(smoothspec[i])/len(smoothspec[i])
		smoothspec[i]=subrtn.normalise(smoothspec[i], delta_norm)
	print 'normalised'





#set some parameters for figures
fig=plt.figure(figsize=(8.3,11.7),dpi=160)
if main_title!='notitle': fig.suptitle(main_title,fontsize=24,fontweight='bold')
fig.subplots_adjust(hspace=0.3,wspace=0.2)
plt.rcParams['font.size']=10

#	ax.axis([wavelength[len(wavelength)-1],wavelength[0],0,fmax])


if len(which_to_plot)==0:
	which_to_plot=[a for a in range(nobs)]

ny=len(which_to_plot)/2

i_cnt=0
#print lmin, lmax
print 'plotting...'
for i in which_to_plot:
	i_cnt=i_cnt+1
		#create spectrum summary figure, with absorption line locations overlaid
	ax=fig.add_subplot(ny+1,1,i_cnt)
	#ax.tick_params(axis='both', which='major', labelsize=10)
	plt.rcParams['text.usetex']='True'
	ax.set_title(raw(labels_to_plot[i_cnt-1]),fontsize=14)
	ax.plot(wavelength[0:-ibin],smoothspec[i], c='k')
	ax.set_ylabel(raw(ylab))
	ax.set_xlabel(raw(xlab))
	#ax.axvline(x=1550, c='r')
        #plt.text(1550,fmin[i],'CIV',fontsize=6)
	#ax.axvline(x=1032, c='b')
	#ax.axvline(x=1038, c='b')
        #plt.text(1038,fmin[i],'OVI',fontsize=6)	
	#ax.axvline(x=1239, c='g')
	#ax.axvline(x=1243, c='g')
        #plt.text(1243,fmin[i],'NV',fontsize=6)
	#ax.axvline(x=1394, c='c')
	#ax.axvline(x=1403, c='c')
        #plt.text(1403,fmin[i],'SiIV',fontsize=6)
	#ax.axvline(x=1026, c='y')
	#ax.axvline(x=1215, c='r')
        #plt.text(1403,fmin[i],'Ly',fontsize=6)

		#ensure that the x axis is scaled within limits specified.
	locator=ax.yaxis.get_major_locator()
	ax.set_autoscale_on(False)
	ax.set_xlim(lmin,lmax)
	locator=ax.yaxis.get_major_locator()
	ax.set_ylim(locator.autoscale())

if (len(sys.argv)>3): 
	#save spectrum summary figure with range given
	plt.savefig(savename+"_range"+str(lmin)+"_"+str(lmax)+'spectrum_sm.'+format,dpi=160,facecolor='w',edgecolor='w',orientation='portrait')

else:
	#save spectrum summary figure
	plt.savefig(savename+'spectrum_sm.'+format,dpi=160,facecolor='w',edgecolor='w',orientation='portrait')



os.system('open -a preview '+savename+'spectrum_sm.'+format)












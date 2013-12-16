import pylab
from math import *
from numpy import *
import os

#input=str(raw_input('Enter input filename:'))
#output=str(raw_input('Enter plot save name:'))
input='nick_stu2010.spec_tot'
output='figure1'

emit=[]
lamdas=[]
nus=[]
surfs=[]
file=open(input, 'r')
i=0
for line in file:
	i=i+1
	if i>44:
		nu,lamda,emitted,censrce,disk,wind,hitsurf,scattered=line.split()
		nus.append(float(nu))
		lamdas.append(float(lamda))
		diff=float(emitted)-float(scattered)
		emit.append(diff)
		surfs.append(float(hitsurf))


truth=int(raw_input('Would you like to do another file, yes(1) or no(0)?:'))


if truth==1:
	#input2=str(raw_input('Enter input filename:'))
	#output2=str(raw_input('Enter plot save name:'))
	input2='nick_stu2010b_test.spec_tot'
	emit2=[]
	lamdas2=[]
	nus2=[]
	surfs2=[]
	file=open(input2, 'r')
	i=0
	for line in file:
		i=i+1
		if i>44:
			nu,lamda,emitted,censrc,disk,wind,hitsurf,scattered=line.split()
			nus2.append(nu)
			lamdas2.append(lamda)
			diff=float(emitted)-float(scattered)
			emit2.append(emitted)
			surfs2.append(hitsurf)
			
pylab.clf()
pylab.plot(nus,emit, c='k')
pylab.xlim([0,1E18)
#pylab.plot(nus2,emit2,c='b')
pylab.xlabel('Frequency')
pylab.savefig(output)
pylab.clf()
pylab.plot(nus,surfs, c='k')
#pylab.plot(nus2,surfs2,c='b')
pylab.savefig(output+'_hitsurf')
os.system('open -a preview '+output+'.png')
os.system('open -a preview '+output+'_hitsurf'+'.png')






			

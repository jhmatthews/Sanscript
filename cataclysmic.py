#!/usr/bin/python
# Filename: cataclysmic.py

# Python Module for use in Cataclysmic Variable Analysis
# Developed by Juan Venancio Hernandez Santisteban
# December 2010--2012
import numpy as n
from scipy import *
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import pyfits as py

def phase(hjd,hjd0,period):
	phase=(hjd-hjd0)/period-n.fix((hjd-hjd0)/period)
	if phase < 0.0:
		phase = phase+1.
	return phase

def trunc(f, n):
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

def spline3(x,a):
    return a[0]*x**3+a[1]*x**2+a[2]*x+a[3]

def func_sin(x,a):
    return a[0]+a[1]*sin(2*n.pi*(x-a[2])/a[3])

def func_sin3(x,a):
    return a[0]+a[1]*sin(2*n.pi*(x-a[2])/par.per)

def func_gauss(x,a):
	return a[0]*n.exp(-(a[1]-x)**2/(2*a[2]**2))+a[3]

def res_gauss(a,y,x):
	 err = y-func_gauss(x,a)
	 return err
 
def residuals(a, y, x):
    err = y-func_sin(x,a)
    return err

def residuals3(a, y, x):
    err = y-func_sin3(x,a)
    return err

def residuals_spl3(a, y, x):
    err = y-spline3(x,a)
    return err

def phase1(hjd,hjd0,period):
	phase=[]
	for i in hjd:
		tmp=(i-hjd0)/period-n.fix((i-hjd0)/period)
		if tmp < 0.0:
			tmp = tmp+1.
		phase.append(tmp)
	phase1=array(phase)
	return phase1

def orbital(x,y,a):
    yfit = leastsq(residuals, a, args=(y, x), maxfev=2000)
    return yfit

def orbital3(x,y,a):
    yfit = leastsq(residuals3, a, args=(y, x), maxfev=2000)
    return yfit

def gaussianfit(x,y,a):
	yfit = leastsq(res_gauss,a,args=(y,x),maxfev=2000)
	return yfit
def read_xshooter(name,plot):
    ## Read Xshooter spectra. Plotting capability
    hdulist=py.open(name)
    ##hdulist.info()
    w1delta=py.getval(name,'CDELT1',0)
    w1start=py.getval(name,'CRVAL1',0)
    flux=py.getdata(name)
    wave=[]
    n=len(flux)
    for i in range(n):
        wave.append((i-1)*w1delta+w1start)
    if plot == 1:
        plt.plot(wave,flux)
        plt.axis([min(wave),max(wave),-1e-17,max(flux)])        
    hdulist.close()
   # print len(wave),len(flux)
    return(wave,flux)

def jfilter(wave,flux,filt):
    ## Calculate equivalente Johnson filter magnitude from spectra
    ## Returns magnitude
    if filt == 'U':
        cen_wav=365.00  ## nanometers
        del_wav=33.00   ## nanometers
    if filt == 'B':
        cen_wav=445.00  ## nanometers
        del_wav=47.00   ## nanometers
    if filt == 'V':
        cen_wav=551.00  ## nanometers
        del_wav=44.00   ## nanometers
    if filt == 'R':
        cen_wav=658.00  ## nanometers
        del_wav=69.00   ## nanometers
    if filt == 'I':
        cen_wav=806.00  ## nanometers
        del_wav=74.50   ## nanometers
    if filt == 'J':
        cen_wav=1220.00  ## nanometers
        del_wav=106.50   ## nanometers
    if filt == 'H':
        cen_wav=1630.00  ## nanometers
        del_wav=153.50   ## nanometers
    if filt == 'K':
        cen_wav=2190.00  ## nanometers
        del_wav=195.00   ## nanometers
    flux_tot=0.0
    for i,j in zip(wave,flux):
        if i > cen_wav-del_wav and i< cen_wav+del_wav:
            flux_tot=flux_tot+j
    mag=-2.5*n.log10(flux_tot)
    return(mag)

def wdmodel(temp,logg,ex):
    if temp > 60000 or temp < 8000:
        print 'ERROR: Temperature out of range'
    if temp >= 10000 and temp<= 60000:
        wave,flux=n.loadtxt('/Users/juan/astro/WD/spectra'+str(logg)+'/h0'+str(temp)+'g'+str(logg)+'0.'+str(ex),unpack=True)
    if temp < 10000 and temp >= 8000:
        wave,flux=n.loadtxt('/Users/juan/astro/WD/spectra'+str(logg)+'/h00'+str(temp)+'g'+str(logg)+'0.'+str(ex),unpack=True)
    return(wave,flux)


def redshift(wave,vel):
    #velocity should be in km/s
    return(wave/(1+vel/299000.0))

def medfilt1(x=None,L=None):

    '''
    a simple median filter for 1d numpy arrays.

    performs a discrete one-dimensional median filter with window
    length L to input vector x. produces a vector the same size 
    as x. boundaries handled by shrinking L at edges; no data
    outside of x used in producing the median filtered output.
    (upon error or exception, returns None.)

    inputs:
        x, Python 1d list or tuple or Numpy array
        L, median filter window length
    output:
        xout, Numpy 1d array of median filtered result; same size as x
    
    bdj, 5-jun-2009
    '''

    # input checks and adjustments --------------------------------------------
    try:
        N = len(x)
        if N < 2:
            print 'Error: input sequence too short: length =',N
            return None
        elif L < 2:
            print 'Error: input filter window length too short: L =',L
            return None
        elif L > N:
            print 'Error: input filter window length too long: L = %d, len(x) = %d'%(L,N)
            return None
    except:
        print 'Exception: input data must be a sequence'
        return None

    xin = n.array(x)
    if xin.ndim != 1:
        print 'Error: input sequence has to be 1d: ndim =',xin.ndim
        return None
    
    xout = n.zeros(xin.size)

    # ensure L is odd integer so median requires no interpolation
    L = int(L)
    if L%2 == 0: # if even, make odd
        L += 1 
    else: # already odd
        pass 
    Lwing = (L-1)/2

    # body --------------------------------------------------------------------

    for i,xi in enumerate(xin):
  
        # left boundary (Lwing terms)
        if i < Lwing:
            xout[i] = n.median(xin[0:i+Lwing+1]) # (0 to i+Lwing)

        # right boundary (Lwing terms)
        elif i >= N - Lwing:
            xout[i] = n.median(xin[i-Lwing:N]) # (i-Lwing to N-1)
            
        # middle (N - 2*Lwing terms; input vector and filter window overlap completely)
        else:
            xout[i] = n.median(xin[i-Lwing:i+Lwing+1]) # (i-Lwing to i+Lwing)

    return xout

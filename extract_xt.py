# -- coding: utf-8 --
import math
import sdf
import matplotlib
import math
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from numpy import ma
from matplotlib import colors, ticker, cm
from matplotlib.mlab import bivariate_normal
from scipy.interpolate import spline
  
if __name__ == "__main__":
  ######## Constant defined here ########
  pi        =     3.1415926535897932384626
  q0        =     1.602176565e-19 # C
  m0        =     9.10938291e-31  # kg
  v0        =     2.99792458e8    # m/s^2
  kb        =     1.3806488e-23   # J/K
  mu0       =     4.0e-7*pi       # N/A^2
  epsilon0  =     8.8541878176203899e-12 # F/m
  h_planck  =     6.62606957e-34  # J s
  wavelength=     1.0e-6
  frequency =     v0*2*pi/wavelength
  micron    =     1.0e-6
  c         =     3e8
  exunit    =     m0*v0*frequency/q0
  bxunit    =     m0*frequency/q0
  denunit    =     frequency**2*epsilon0*m0/q0**2
  print 'electric field unit: '+str(exunit)
  print 'magnetic field unit: '+str(bxunit)
  print 'density unit nc: '+str(denunit)
  
  font = {'family' : 'monospace',  
          'color'  : 'black',  
          'weight' : 'normal',  
          'size'   : 28,  
          }  
  
  
  
  ######### Parameter you should set ###########
  dirsdf  =  '../Data/delaylaser/'
  dirsize =  4

#####
  c       =  3e8
  micron  =  1e-6 
  x_max   =  60 * micron
  x_min   =  0 * micron
  window_start_time =  (x_max - x_min) / c 
  start_move_number =  int(window_start_time * 1e15)
  y       =  1250
  x_end   =  60 * micron
  gridnumber = 2400
  delta_x =  x_end/gridnumber
  start   =  1  # start time
  stop    =  1000  # end time
  step    =  1  # the interval or step
  dt_snapshot= 1e-15  #fs
  dt      =  dt_snapshot*1e15  #fs
  t_end   =  stop * dt_snapshot
  t_n     =  int(t_end/1e-15)
  if t_end-window_start_time<0:
      xgrid   =  int(gridnumber)
  else:
      xgrid   =  int(gridnumber + c*(t_end-window_start_time)/delta_x)
   
  if (os.path.isdir('fft') == False):
    os.mkdir('fft')
  if (os.path.isdir('txt') == False):
    os.mkdir('txt')
  ######### Script code drawing figure ################
 
####################

  x_interval=1
  t_total=1e15*x_end/c         #fs
  t_size=int(t_total/dt)+1+1   

######allay define
  xt=np.zeros((int(xgrid/x_interval)+1,t_size))

  for n in range(start,stop+step,step):
        #### header data ####
        data = sdf.read(dirsdf+str(n).zfill(dirsize)+".sdf",dict=True)
        header=data['Header']
        time=header['time']
        if  n  <  start_move_number:
                     
           for x in range(1,int(gridnumber/x_interval)+1):
              a=int(x*x_interval)
              d_n=int((1e15*delta_x*a/c)/dt)
              if n-d_n > 0 and n-d_n < t_size :
                    #[fs]
                   xt[x][n-d_n]=data['Magnetic Field/Bz'].data[a-1][y]/bxunit            
        else:
           for x in range(1,int(xgrid/x_interval)+1):
                
             #if x > 1200 :
               a=int(x*x_interval)
	       if a-c*(time-window_start_time)/delta_x >= 0 and a-c*(time-window_start_time)/delta_x < gridnumber-1:
		    #[fs]
                   d_n=int((1e15*delta_x*a/c)/dt)
                   xt[x][n-d_n]=data['Magnetic Field/Bz'].data[int(round(a-c*(time-window_start_time)/delta_x))][y]/bxunit
                   #else:bz.append(0)
                   #print 'Reading finished%d' %len(t)
  
  np.savetxt("./txt/xt.txt", xt)


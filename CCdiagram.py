# -*- coding: utf-8 -*-
import glob
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy.integrate import quad


band_g = []
band_i = []
band_r = []
band_u = []
band_z = []

def sdss_mod(x): #product of mod and sys lines
    return f_linear(x) * s_linear(x) 
models = glob.glob('*Gyr')
sdss = sorted(glob.glob('sys.*'))
sys_count = 0 
for file in sdss:
    file = np.loadtxt(file)
    sys_x = file[:,0]
    sys_y = file[:,1]
    s_linear = interp1d(sys_x,sys_y,fill_value='extrapolate')
    #iterate over all model spectra 
    sys_count += 1 
    #print(sys_count) #used to make sure all sdss files were iterated over
    for model in models:
        model = np.loadtxt(model)
        x = model[:,0]
        y = model[:,1]
        f_linear = interp1d(x,y,fill_value='extrapolate')
        I, err = quad(sdss_mod, min(sys_x), max(sys_y))
        I2, err2 = quad(s_linear, min(sys_x), max(sys_y))
        f = I/I2 #flux

        magnitude = (-2.5*(np.log10(f)))-48.6 #magnitude of each model
        if sys_count == 1:
            band_g.append(magnitude)
        elif sys_count == 2:
            band_i.append(magnitude)
        elif sys_count == 3:
            band_r.append(magnitude)    
        elif sys_count == 4:
            band_u.append(magnitude)
        elif sys_count == 5:
            band_z.append(magnitude)
#subtract band arrays to obtain data for color-color diagram            
xmain = list(np.array(band_r) - np.array(band_g)) #choose desired bands
ymain = list(np.array(band_i) - np.array(band_r)) #choose desired bands  

plt.figure()
plt.xlabel('R - G')
plt.ylabel('I - R')
plt.title('Color-Color Diagram')
plt.plot(xmain, ymain,'k--',)
#plt.savefig('CCD1')
plt.show()    

            


                        
            
            
        














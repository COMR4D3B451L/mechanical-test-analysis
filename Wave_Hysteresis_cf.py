###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import numpy as np
import numpy
import pylab as pl
import matplotlib.pyplot as plt
import csv
import math
import scipy
from scipy.optimize import curve_fit
from numpy.polynomial import polynomial as P



# Specimen Matrix for Parameters in mm and file name (Length, Width, Thickness, file name)

groupA = [[30, 10.06, 4.91, './csvCyclicStrainCyclicBufferReadout/A_CS_Y_66_20190530CyclicBufferReadout', 5]]
groupB = [[30, 10.14, 5.12, './csvCyclicStrainCyclicBufferReadout/B_CS_Y_67_20190530CyclicBufferReadout', 5]]
groupC = [[30, 10.17, 4.73, './csvCyclicStrainCyclicBufferReadout/C_CS_BK_68_20190530CyclicBufferReadout', 5]]
groupDY = [[30, 10.13, 5.33, './csvCyclicStrainCyclicBufferReadout/D_CS_Y_69_20190530CyclicBufferReadout', 5]]
groupDBK = [[30, 10.07, 4.76, './csvCyclicStrainCyclicBufferReadout/D_CS_BK_70_20190530CyclicBufferReadout', 5]]

ACStrs = [[30, 10.08, 4.64, './csvCyclicBufferReadout/A_F_Y_7_20190509CyclicBufferReadout', 10]]
BCStrs = [[30, 10.11, 5.15, './csvCyclicBufferReadout/B_F_Y_18_20190514CyclicBufferReadout', 15]]
CCStrs = [[30, 10.11, 5.15, './csvCyclicBufferReadout/C_F_BK_30_20190515CyclicBufferReadout', 15]]
DYCStrs = [[30, 10.12, 5.25, './csvCyclicBufferReadout/D_F_Y_42_20190517CyclicBufferReadout', 15]]
DBKCStrs = [[30, 10.09, 4.78, './csvCyclicBufferReadout/D_F_BK_56_20190521CyclicBufferReadout', 15]]

parameters = DYCStrs
group = 'Group A'

# Use 2-4, 3-5, 4-6, 5-7, 6-8 to change the location of lines
tweak1 = 2
tweak2 = 4
# Vertical distance between a stress point and a strain point
tweak3 = .06

# Extracting parameters to be used in SS function
L = [row[0] for row in parameters]
W = [row[1] for row in parameters]
T = [row[2] for row in parameters]
file = [row[3] for row in parameters]
freq = [row[4] for row in parameters]

# Import the test data from csv file (Time, Force, Displacement)

def OpenFile(file):
    global data
    data = csv.reader(open(file+'.csv', 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')
    return data

def CCurve(L, W, T, data, group, freq):

    # Arrays
    time, dis, forceSignal, force, segments, stress, strain = [], [], [], [], [], [], []
    area = W * T

    for row in data:
        time.append(row[1])
        dis.append(row[4])
        force.append(row[3])
        segments.append(row[5])
        stress.append(row[3] / area)
        strain.append(((row[4])) / L)

    # What data do we want to work with
    xac = time
    yac = stress
    zac = strain
    # plotting the main values
    xxac = xac[len(xac)-150:len(xac)]
    yyac = yac[len(yac)-150:len(yac)]
    zzac = zac[len(zac)-150:len(zac)]

    mean_stress_ac = (min(stress)+max(stress))/2
    mean_strain_ac = (min(strain)+max(strain))/2
    amp_stress_ac = (min(stress)-max(stress))/2
    amp_strain_ac = (min(strain)-max(strain))/2

    # Normalizing data to range 0-1
    x, y, z = [], [], []
    for i in range(0,len(time)):
       x.append((time[i]-min(time))/(max(time)-min(time)))
    for i in range(0,len(force)):
       y.append((force[i]-min(force))/(max(force)-min(force)))
    for i in range(0,len(dis)):
       z.append((dis[i]-min(dis))/(max(dis)-min(dis)))


    # plotting the main values
    xx = x[len(x)-150:len(x)]
    yy = y[len(y)-150:len(y)]
    zz = z[len(z)-150:len(z)]

    # Calculating the phase angle difference between stress and strain
    seg1 = segments.index(min(segments)+tweak1) # Tweek the numbers for better position on the curve
    seg2 = segments.index(min(segments)+tweak2) # Tweek the numbers for better position on the curve

    xxx = x[seg1:seg2]
    yyy = y[seg1:seg2]
    zzz = z[seg1:seg2]

    mean_stress = (min(yyy)+max(yyy))/2
    mean_strain = (min(zzz)+max(zzz))/2

    xb = np.asarray(xx)
    yb = np.asarray(yy)

    coeff, stats = P.polyfit(xb, yb, 9, full = True)
    fitpoly = P.Polynomial(coeff)

    fitfunc = lambda x, a, b: a * np.sin(b * x)
    p, pcov = curve_fit(fitfunc, xb, yb, p0 = [1.0, 1.0])

    yi = []
    for i in range (0, len(xx)):
        yi.append(p[0] * np.sin(p[1] * xx[i]*15*3)+.5)

    plt.plot(xb, yb, color = 'r')
    plt.plot(xx, yi, color = 'b')

    plt.show()


# Defining global variables
data = "global"

for files in range(0, len(file)):
    OpenFile(file[files])
    plot = CCurve(L[files], W[files], T[files], data, group, freq[files])


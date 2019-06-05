###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import csv
import math

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

parameters = ACStrs
group = 'Group DBK'

# Use 2-4, 3-5, 4-6, 5-7, 6-8 to change the location of lines
tweak1 = 2
tweak2 = 4

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

    print('Mean stress = ', mean_stress_ac)
    print('Mean strain = ', mean_strain_ac)


    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], array[idx+1]

    sit = find_nearest(yyy, mean_stress)
    sat = find_nearest(zzz, mean_strain)
    tim = xxx[yyy.index(sit[0])]
    timm = xxx[yyy.index(sit[0])+1]
    tim1 =(tim, timm)
    p1 = (sit[0], tim1[0])
    p2 = (sit[1], tim1[1])

    p3 = (sat[0], tim1[0])
    p4 = (sat[1], tim1[1])

    def getEquidistantPoints(p1, p2, parts):
        return zip(np.linspace(p1[0], p2[0], parts + 1), np.linspace(p1[1], p2[1], parts + 1))

    lines = list(getEquidistantPoints(p1, p2, 100))
    lines2 = list(getEquidistantPoints(p3, p4, 100))


    x_val = [x[1] for x in lines]
    y_val = [x[0] for x in lines]
    x1_val = [x[1] for x in lines2]
    y1_val = [x[0] for x in lines2]
    tweak3 = sit[0]-sat[0]
    index1 = y_val.index(find_nearest(y_val, mean_stress)[0])
    index2 = y1_val.index(find_nearest(y1_val, mean_strain+tweak3)[0]) # Tweek the number for adjusting to the distance between two points
    time1 = x_val[index1]
    time2 = x1_val[index2]
    deltat = time2 - time1
    print('Indexes of stress, strain: ', index1, index2)

    # Viscoelastic properties

    delta = (2*np.pi*deltat)/(1/freq)
    tand = math.tan(math.radians(delta))
    complex_modulus = amp_stress_ac/amp_strain_ac
    storage_modulus = complex_modulus*math.cos(math.radians(delta))
    loss_modulus = complex_modulus*math.sin(math.radians(delta))

    print('Phase shift = ', str(deltat) + ' Sec')
    print('Phase difference = ', str(delta) +' Degrees')
    print('Damping ratio = ', tand)
    print('Complex Modulus = ', str(complex_modulus) + ' MPa')
    print('Storage Modulus = ', str(storage_modulus) + ' MPa')
    print('Loss Modulus = ', str(loss_modulus) + ' MPa')


    # Plots
    plt.figure(1)
    plt.plot(xxac, yyac, color = 'blue', label = 'Stress')
    pl.legend(loc = 'lower right')
    pl.ylabel('Engineering Stress (MPa)')
    pl.xlabel('Time (Sec)')
    plt.axhline(y = ((min(yyac)+max(yyac))/2), color = 'black', alpha = 0.5)

    pl.twinx()
    plt.plot(xxac, zzac, color = 'red', label = 'Strain')
    pl.legend(loc = 'upper right')
    pl.ylabel('Engineering Strain (mm/mm)')

    plt.grid(True)
    pl.title('Cyclic Loading Wave for ' + group)


    plt.figure(2)
    plt.plot(zz, yy, color = 'blue', label = 'Stress-Srain')
    pl.title('Hysteresis Loop for ' + group)
    pl.xlabel('Engineering Strain (mm/mm)')
    pl.ylabel('Engineering Stress (MPa)')

    plt.grid(True)

    plt.figure(3)
    plt.plot(xxx, yyy, color = 'blue', label = 'Stress', marker = '.')
    pl.legend(loc = 'lower right')
    pl.ylabel('Engineering Stress (MPa)')
    pl.xlabel('Time (Sec)')
    plt.axhline(y = ((min(yyy)+max(yyy))/2), color = 'blue', alpha = 0.5)

    plt.scatter(x_val, y_val)


    # pl.twinx()
    plt.plot(xxx, zzz, color = 'red', label = 'Strain', marker = '.')
    pl.legend(loc = 'upper right')
    pl.ylabel('Normalized Stress, Strain')
    plt.grid(True)
    pl.title('Cyclic Loading Wave for ' + group)
    plt.axhline(y = ((min(zzz)+max(zzz))/2), color = 'red', alpha = 0.5)


    plt.scatter(x1_val, y1_val)


# Defining global variables
data = "global"

for files in range(0, len(file)):
    OpenFile(file[files])
    plot = CCurve(L[files], W[files], T[files], data, group, freq[files])

pl.show()

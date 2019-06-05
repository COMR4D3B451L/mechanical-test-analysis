###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################


import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import csv
import random
from numpy import array

# Specimen Matrix for Parameters in mm and file name (Length, Width, Thickness, file name)


group1500 = [[30, 10.06, 4.91, 'A_C1_Y_66_20190530', 1500],
              [30, 10.14, 5.12, 'B_C1_Y_67_20190530', 1400],
              [30, 10.17, 4.73, 'C_C1_BK_68_20190530', 1500],
              [30, 10.13, 5.33, 'D_C1_Y_69_20190530', 1500],
              [30, 10.07, 4.76, 'D_C1_BK_70_20190530', 1500]]

group1350 = [[30, 10.06, 4.91, 'A_C2_Y_66_20190530', 1350],
              [30, 10.14, 5.12, 'B_C2_Y_67_20190530', 1200],
              [30, 10.17, 4.73, 'C_C2_BK_68_20190530', 1350],
              [30, 10.13, 5.33, 'D_C2_Y_69_20190530', 1350],
              [30, 10.07, 4.76, 'D_C2_BK_70_20190530', 1500]]

group1200 = [[30, 10.06, 4.91, 'A_C3_Y_66_20190530', 1200],
              [30, 10.14, 5.12, 'B_C3_Y_67_20190530', 1000],
              [30, 10.17, 4.73, 'C_C3_BK_68_20190530', 1200],
              [30, 10.13, 5.33, 'D_C3_Y_69_20190530', 1200],
              [30, 10.07, 4.76, 'D_C3_BK_70_20190530', 1200]]

parameters = group1500
group = 'all groups'

# Extracting parameters to be used in SS function
L = [row[0] for row in parameters]
W = [row[1] for row in parameters]
T = [row[2] for row in parameters]
file = [row[3] for row in parameters]
stressLevel = [row[4] for row in parameters]



# Import the test data from csv file (Time, Force, Displacement)

def OpenFile(file):
    global data
    data = csv.reader(open('./csvCreep/' + file + '.csv', 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')
    return data

# Curve generating function

def SSCurve(L, W, T, data, file, i, group):

    # Global variables
    global strs
    global strn
    global e

    # Arrays
    time, force, dis, stress, strain = [], [], [], [], []
    area = W * T

    for row in data:
        time.append(row[1])
        force.append(row[2])
        dis.append(row[3])
        stress.append(row[2] / area)
        strain.append(((row[3])) / L)

    # What data do we want to work with
    x = time
    y = strain
    e = array(stress)/array(strain)

    for items in x:
        float(items)
    for items in y:
        float(items)

    # plotting the main values
    plt.figure(1)
    marker = ['.']
    color = ['r', 'b', 'y', 'g', 'k', 'm']
    pl.plot(x, y, data = data,
            label = file + ' | Applied Force = ' + str(stressLevel[i]),
            color= random.shuffle(color))
    plt.grid(True)

    # Plot Labels
    pl.ylabel('Engineering Strain (mm/mm)')
    pl.xlabel('Time (sec)')
    pl.title('Creep curve for ' + group)

    plt.figure(2)
    marker = ['.']
    color = ['r', 'b', 'y', 'g', 'k', 'm']
    pl.plot(x, e, data = data,
            label = file + ' | Applied Force = ' + str(stressLevel[i]),
            color= random.shuffle(color))
    plt.grid(True)

    # Plot Labels

    pl.ylabel('Creep Modulus MPa')
    pl.xlabel('Time (sec)')
    pl.title('Creep Modulus curve for ' + group)


    # For auto-resizing according to the biggest graph
    strs = max(y)
    strn = max(x)


    # Fit plot
    # pl.plot(x, fit1(x), color= random.shuffle(color))



    # Print file name

    print("######## Data for Specimen ########")
    print(file)
    print("###################################")


    # Data from test


    print("############## END ################", "\n")


# Defining global variables
data = "global"
strs = "global"
strn = "global"
max_strs, max_strn = [], []

for files in range(0, len(file)):
    OpenFile(file[files])
    plot = SSCurve(L[files], W[files], T[files], data, file[files], files, group)
    max_strs.append(strs)
    max_strn.append(strn)


plt.figure(1)
plt.xlim(0, max(max_strn) * 1.1)
plt.ylim(0, max(max_strs) * 1.1)
pl.legend(loc='lower left')

plt.figure(2)
plt.xlim(1, 620)
plt.ylim(0, 1100)

# Legend and show
pl.legend(loc='lower left')
pl.show()


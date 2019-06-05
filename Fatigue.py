###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import csv
import random
from numpy import polyder

# Specimen Matrix for Parameters in mm and file name (Length, Width, Thickness, file name)

parameters = [[30, 10.07, 4.58, './csv/A_F_Y_6_20190509.csv'],
              [30, 10.08, 4.64, './csv/A_F_Y_7_20190509.csv'],
              [30, 10.07, 4.6, './csv/A_F_Y_8_20190509.csv'],
              [30, 10.07, 4.62, './csv/A_F_Y_9_20190509.csv'],
              [30, 10.12, 4.64, './csv/A_F_Y_10_20190510.csv'],
              [30, 10.17, 4.64, './csv/A_F_Y_11_20190510.csv'],
              [30, 10.11, 4.56, './csv/A_F_Y_12_20190510.csv'],
              [30, 10.14, 4.58, './csv/A_F_Y_13_20190510.csv'],
              [30, 10.09, 4.58, './csv/A_F_Y_14_20190510.csv']]

# Extracting parameters to be used in SS function
L = [row[0] for row in parameters]
W = [row[1] for row in parameters]
T = [row[2] for row in parameters]
file = [row[3] for row in parameters]


# Import the test data from csv file (Time, Force, Displacement)

def OpenFile(file):
    global data
    data = csv.reader(open(file, 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')
    return data


def FCurve(L, W, T, data, file):

    # Global variables
    global strs
    global strn

    # Arrays
    time, dis, forceSignal, force, segments, stress, strain = [], [], [], [], [], [], []
    area = W * T

    for row in data:
        time.append(row[1])
        dis.append(row[2])
        forceSignal.append(row[3])
        force.append(row[4])
        segments.append(row[5])
        stress.append(row[4] / area)
        strain.append(((row[2])) / L)

    # What data do we want to work with
    x = time
    y = stress
    # plotting the main values

    pl.plot(x, y, data = data, marker = '.', color = 'blue')

    print(float(sum(forceSignal)) / max(len(forceSignal), 1))

    strs = max(y)
    strn = max(x)


    # Plot Labels
    pl.ylabel('Engineering Stress (MPa)')
    pl.xlabel('Engineering Strain (mm/mm)')
    pl.title('Stress-Strain curve')




    # Legend and show
    plt.legend(['Virgin PDCPD', 'Fit'], )


# Defining global variables
data = "global"

for files in range(0, len(file)):
    OpenFile(file[files])
    plot = FCurve(L[files], W[files], T[files], data, file[files])


# Legend and show
pl.legend(loc='lower right')
pl.show()

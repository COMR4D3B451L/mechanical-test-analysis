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

group1 = [[30, 10.07, 4.83, 'A_S_Y_1_20190506', 'Virgin'],
              [30, 10.17, 5.14, 'B_S_Y_3_20190506', '2013'],
              [30, 10.1, 4.71, 'C_S_BK_5_20190506', '2012'],
            [30, 10.08, 5.25, 'D_S_Y_4_20190506', '2002 Y'],
            [30, 10.13, 4.8, 'D_S_BK_2_20190506', '2002 BK']]

group2 = [[30, 10.06, 4.91, 'A_S_Y_76_20190603'],
              [30, 10.14, 5.12, 'B_S_Y_77_20190603'],
              [30, 10.17, 4.73, 'C_S_BK_78_20190603'],
              [30, 10.13, 5.33, 'D_S_Y_79_20190603'],
              [30, 10.07, 4.76, 'D_S_BK_80_20190603']]

group3 = [[30, 10.07, 5.04, 'A_S_Y_71_20190603'],
              [30, 10.14, 5.12, 'B_S_Y_72_20190603'],
              [30, 10.17, 4.88, 'C_S_BK_73_20190603'],
              [30, 10.18, 5.19, 'D_S_Y_74_20190603'],
              [30, 10.11, 4.77, 'D_S_BK_75_20190603']]

dic = [[30, 10.07, 5.04, 'ASY71_20190603'],
              [30, 10.14, 5.12, 'BSY72_20190603'],
              [30, 10.17, 4.88, 'CSBK73_20190603'],
              [30, 10.18, 5.19, 'DSY74_20190603'],
              [30, 10.11, 4.77, 'DSBK75_20190603']]

parameters = dic

# Extracting parameters to be used in SS function
L = [row[0] for row in parameters]
W = [row[1] for row in parameters]
T = [row[2] for row in parameters]
file = [row[3] for row in parameters]
year = [row[4] for row in group1]


# Import the test data from csv file (Time, Force, Displacement)

def OpenFile(file):
    global data
    data = csv.reader(open('./csvStatic/' + file + '.csv', 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')
    return data

# Curve generating function

def SSCurve(L, W, T, data, file):

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
    x = strain
    y = stress

    for items in x:
        float(items)
    for items in y:
        float(items)

    # Degrees of polynomial regression (1 for linear regression)
    for degree in range(10):
        degree = degree + 1

        # Polynomial Regression
        z = np.polyfit(x, y, degree)
        p = np.poly1d(z)

        # R SQUARE VALUE
        yhat = p(x)
        ybar = np.sum(y) / len(y)
        ssreg = np.sum((yhat - ybar) ** 2)
        sstot = np.sum((y - ybar) ** 2)  #
        r2 = ssreg / sstot

        if (r2 > 0.99998):
            break

    # Finding the index of values between 0.0004 and 0.0006 (to reach 0.0005)
    value = 0
    for strn in x:
        if 0.0004 <= strn <= 0.0006:
            value = strn
            break
    idx05 = x.index(value)

    # Finding the index of values between 0.002 and 0.003 (to reach 0.0025)
    value1 = 0
    for strn1 in x:
        if 0.0024 <= strn1 <= 0.0026:
            value1 = strn1
            break
    idx25 = x.index(value1)

    # Linear Regression2
    x_linear = x[idx05:idx25]
    y_linear = y[idx05:idx25]
    z1 = np.polyfit(x_linear, y_linear, 1)

    # Linear Regression3
    x_linear2 = x[int(len(x) * 0.05):int(len(x) * 0.25)]
    y_linear2 = y[int(len(x) * 0.05):int(len(x) * 0.25)]
    z2 = np.polyfit(x_linear2, y_linear2, 1)

    # the polynomial equations:
    fit1 = p
    fit2 = np.poly1d(z1)
    fit3 = np.poly1d(z2)

    # Differentiation of 1st polynomial
    diff_fit1 = polyder(fit1, 1)
    x_diff = []
    x_diff.append(diff_fit1(x))
    delta = np.diff(x_diff)

    # Differentiation of 2nd polynomial
    slope = polyder(fit2, 1)

    # Differentiation of 3nd polynomial
    slope2 = polyder(fit3, 1)

    # plotting the main values
    plt.figure(1)
    marker = [',', '+', '3', '1', '*', '2']
    color = ['r', 'b', 'y', 'g', 'k', 'm']
    pl.plot(x, y, data = data,
            label = file, marker = random.choice(marker),
            color= random.shuffle(color))
    plt.grid(True)
    pl.legend(loc = 'lower right')

    # Plot Labels
    pl.ylabel('Engineering Stress (MPa)')
    pl.xlabel('Engineering Strain (mm/mm)')
    pl.title('Stress-Strain curve')

    # Plot borders
    plt.xticks([0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.2,
                0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34])
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 100,
                110, 120, 130, 140, 150])

    # For auto-resizing according to the biggest graph
    strs = max(stress)
    strn = max(strain)

    ''' (Only enable when needed)
    # Fit plot
    # pl.plot(x, fit1(x), "r-")

    # Fit2 Plot 
    
    pl.plot(x, fit2(x), "g-")
    Fit3 Plot
    pl.plot(x, fit3(x), "y-")
    '''

    # Print file name

    print("####### Data for Specimen #######")
    print(file)
    print("################################")

    # R Square Value of the main fit
    # print("r-Square for the fit = ", r2)

    # Degrees
    # print("Fit polynomial degree = ", degree)

    # Data from test
    print("Ultimate Strength = ", max(y), "MPa")
    print("Ultimate Force = ", max(force), "N")
    print("Stress at Failure =", y[-1], "MPa")
    print("force at Failure =", force[-1], "N")
    print("Strain at Failure =", x[-1], "mm/mm")
    print("Displacement at Failure =", dis[-1], "mm")
    print("Young's Modulus Range:", slope, "MPa (ISO Slope)", slope2, "MPa (Slope)")
    e = str(slope2)
    e = float(e)
    print("########### END #############", "\n")


# Defining global variables
data = "global"
strs = "global"
strn = "global"
e = "global"
max_strs, max_strn, e_list = [], [], []

for files in range(0, len(file)):
    OpenFile(file[files])
    plot = SSCurve(L[files], W[files], T[files], data, file[files])
    max_strs.append(strs)
    max_strn.append(strn)
    e_list.append(e)

plt.figure(1)
plt.xlim(0, max(max_strn) * 1.1)
plt.ylim(0, max(max_strs) * 1.1)

plt.figure(2)
plt.plot(year, e_list, 'r--')


# Legend and show
pl.show()


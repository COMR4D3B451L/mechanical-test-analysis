###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import matplotlib.pyplot as plt
import csv
import numpy as np
import random
import pandas as pd
import math
import seaborn as sns
from scipy.optimize import curve_fit

# Specimen Matrix for Parameters in mm and file name (Length, Width, Thickness, file name, 1 = failed & 0 = not failed)

folder = './csvCyclicStress/'

groupA = [[30, 10.07, 4.58, 'A_F_Y_6_20190509', 'A_F_Y_6_20190509CyclicBufferReadout', 1],
              [30, 10.08, 4.64, 'A_F_Y_7_20190509', 'A_F_Y_7_20190509CyclicBufferReadout', 1],
              [30, 10.07, 4.6, 'A_F_Y_8_20190509', 'A_F_Y_8_20190509CyclicBufferReadout', 1],
              [30, 10.07, 4.62, 'A_F_Y_9_20190509', 'A_F_Y_9_20190509CyclicBufferReadout', 0],
              [30, 10.12, 4.64, 'A_F_Y_10_20190510', 'A_F_Y_10_20190510CyclicBufferReadout', 1],
              [30, 10.17, 4.64, 'A_F_Y_11_20190510', 'A_F_Y_11_20190510CyclicBufferReadout', 1],
              [30, 10.11, 4.56, 'A_F_Y_12_20190510', 'A_F_Y_12_20190510CyclicBufferReadout', 1],
              [30, 10.14, 4.58, 'A_F_Y_13_20190510', 'A_F_Y_13_20190510CyclicBufferReadout', 1],
              [30, 10.09, 4.58, 'A_F_Y_14_20190510', 'A_F_Y_14_20190510CyclicBufferReadout', 1],
              [30, 10.06, 5.06, 'A_F_Y_15_20190513', 'A_F_Y_15_20190513CyclicBufferReadout', 1],
              [30, 10.06, 4.94, 'A_F_Y_16_20190513', 'A_F_Y_16_20190513CyclicBufferReadout', 1],
              [30, 10.1, 5.31, 'A_F_Y_17_20190513', 'A_F_Y_17_20190513CyclicBufferReadout', 0]]

groupB = [[30, 10.11, 5.15, 'B_F_Y_18_20190514', 'B_F_Y_18_20190514CyclicBufferReadout', 1],
              [30, 10.09, 5.14, 'B_F_Y_19_20190514', 'B_F_Y_19_20190514CyclicBufferReadout', 1],
              [30, 10.12, 5.16, 'B_F_Y_20_20190514', 'B_F_Y_20_20190514CyclicBufferReadout', 1],
              [30, 10.07, 5.1, 'B_F_Y_21_20190514', 'B_F_Y_21_20190514CyclicBufferReadout', 1],
              [30, 10.15, 5.1, 'B_F_Y_22_20190514', 'B_F_Y_22_20190514CyclicBufferReadout', 1],
              [30, 10.08, 5.12, 'B_F_Y_23_20190514', 'B_F_Y_23_20190514CyclicBufferReadout', 0],
              [30, 10.04, 5.14, 'B_F_Y_24_20190514', 'B_F_Y_24_20190514CyclicBufferReadout', 1],
              [30, 10.13, 5.11, 'B_F_Y_25_20190514', 'B_F_Y_25_20190514CyclicBufferReadout', 1],
              [30, 10.04, 5.13, 'B_F_Y_26_20190515', 'B_F_Y_26_20190515CyclicBufferReadout', 1],
              [30, 10.08, 5.09, 'B_F_Y_27_20190515', 'B_F_Y_27_20190515CyclicBufferReadout', 0],
              [30, 10.07, 5.14, 'B_F_Y_28_20190515', 'B_F_Y_28_20190515CyclicBufferReadout', 1],
              [30, 10.01, 5.12, 'B_F_Y_29_20190515', 'B_F_Y_29_20190515CyclicBufferReadout', 1]]

groupC = [[30, 10.11, 5.15, 'C_F_BK_30_20190515', 'C_F_BK_30_20190515CyclicBufferReadout', 1],
              [30, 10.09, 5.14, 'C_F_BK_31_20190515', 'C_F_BK_31_20190515CyclicBufferReadout', 1],
              [30, 10.12, 5.16, 'C_F_BK_32_20190515', 'C_F_BK_32_20190515CyclicBufferReadout', 1],
              [30, 10.07, 5.1, 'C_F_BK_33_20190515', 'C_F_BK_33_20190515CyclicBufferReadout', 1],
              [30, 10.15, 5.1, 'C_F_BK_34_20190515', 'C_F_BK_34_20190515CyclicBufferReadout', 1],
              [30, 10.08, 5.12, 'C_F_BK_35_20190515', 'C_F_BK_35_20190515CyclicBufferReadout', 1],
              [30, 10.04, 5.14, 'C_F_BK_36_20190516', 'C_F_BK_36_20190516CyclicBufferReadout', 1],
              [30, 10.13, 5.11, 'C_F_BK_37_20190516', 'C_F_BK_37_20190516CyclicBufferReadout', 1],
              [30, 10.04, 5.13, 'C_F_BK_38_20190516', 'C_F_BK_38_20190516CyclicBufferReadout', 1],
              [30, 10.08, 5.09, 'C_F_BK_39_20190516', 'C_F_BK_39_20190516CyclicBufferReadout', 0],
              [30, 10.07, 5.14, 'C_F_BK_40_20190517', 'C_F_BK_40_20190517CyclicBufferReadout', 1],
              [30, 10.01, 5.12, 'C_F_BK_41_20190517', 'C_F_BK_41_20190517CyclicBufferReadout', 0]]

groupDY = [[30, 10.12, 5.25, 'D_F_Y_42_20190517', 'D_F_Y_42_20190517CyclicBufferReadout', 1],
          [30, 10.14, 5.24, 'D_F_Y_43_20190517', 'D_F_Y_43_20190517CyclicBufferReadout', 1],
          [30, 10.16, 5.15, 'D_F_Y_44_20190517', 'D_F_Y_44_20190517CyclicBufferReadout', 1],
          [30, 10.08, 5.28, 'D_F_Y_45_20190517', 'D_F_Y_45_20190517CyclicBufferReadout', 1],
          [30, 10.12, 5.21, 'D_F_Y_46_20190517', 'D_F_Y_46_20190517CyclicBufferReadout', 1],
          [30, 10.09, 5.15, 'D_F_Y_47_20190517', 'D_F_Y_47_20190517CyclicBufferReadout', 1],
          [30, 10.06, 5.19, 'D_F_Y_48_20190520', 'D_F_Y_48_20190520CyclicBufferReadout', 1],
          [30, 10.11, 5.18, 'D_F_Y_49_20190520', 'D_F_Y_49_20190520CyclicBufferReadout', 1],
          [30, 10.09, 5.23, 'D_F_Y_50_20190520', 'D_F_Y_50_20190520CyclicBufferReadout', 1],
          [30, 10.13, 5.27, 'D_F_Y_51_20190520', 'D_F_Y_51_20190520CyclicBufferReadout', 1],
          [30, 10.18, 5.17, 'D_F_Y_52_20190520', 'D_F_Y_52_20190520CyclicBufferReadout', 1],
          [30, 10.09, 5.28, 'D_F_Y_53_20190520', 'D_F_Y_53_20190520CyclicBufferReadout', 0]]

groupDBK = [[30, 10.06, 4.76, 'D_F_BK_54_20190520', 'D_F_BK_54_20190520CyclicBufferReadout', 1],
             [30, 10.06, 4.75, 'D_F_BK_55_20190521', 'D_F_BK_55_20190521CyclicBufferReadout', 1],
             [30, 10.09, 4.78, 'D_F_BK_56_20190521', 'D_F_BK_56_20190521CyclicBufferReadout', 1],
             [30, 10.11, 4.75, 'D_F_BK_57_20190521', 'D_F_BK_57_20190521CyclicBufferReadout', 1],
             [30, 10.15, 4.75, 'D_F_BK_58_20190521', 'D_F_BK_58_20190521CyclicBufferReadout', 1],
             [30, 10.14, 4.76, 'D_F_BK_59_20190521', 'D_F_BK_59_20190521CyclicBufferReadout', 1],
             [30, 10.17, 4.77, 'D_F_BK_60_20190521', 'D_F_BK_60_20190521CyclicBufferReadout', 1],
             [30, 10.08, 4.84, 'D_F_BK_61_20190521', 'D_F_BK_61_20190521CyclicBufferReadout', 1],
             [30, 10.13, 4.77, 'D_F_BK_62_20190521', 'D_F_BK_62_20190521CyclicBufferReadout', 1],
             [30, 10.14, 4.81, 'D_F_BK_63_20190521', 'D_F_BK_63_20190521CyclicBufferReadout', 1],
             [30, 10.11, 4.81, 'D_F_BK_64_20190521', 'D_F_BK_64_20190521CyclicBufferReadout', 0],
             [30, 10.08, 4.80, 'D_F_BK_65_20190521', 'D_F_BK_65_20190521CyclicBufferReadout', 1]]



# Extracting parameters to be used in SS function
parameters = groupDBK
strgroup = "Group D Black"

L = [row[0] for row in parameters]
W = [row[1] for row in parameters]
T = [row[2] for row in parameters]
file = [row[3] for row in parameters]
cycleFile = [row[4] for row in parameters]
failed = [row[5] for row in parameters]



# Import the test data from csv file (Time, Force, Displacement)

def OpenFile(file, cycleFile, folder):
    global data
    global maxCycle

    data = csv.reader(open(folder + file + '.csv', 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')

    cycledata = pd.read_csv('./csvCyclicBufferReadout/' + cycleFile + '.csv', sep = ',', engine = 'python')
    cycledata = cycledata.values
    maxCycle = max(cycledata[:, 5])

    return maxCycle, data


def FCurve(L, W, T, data, file, maxCycle, failed):

    # Global variables
    global maxStress
    global cycles
    global logmaxStress
    global logcycles

    # Arrays
    time, dis, forceSignal, force, stress, strain, segments = [], [], [], [], [], [], []
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

    maxStress = (max(stress) - max(stress)*0.1) / 2 #Stress Amp for R value of 0.1
    cycles = maxCycle / 2
    logmaxStress = math.log10(maxStress)
    logcycles = math.log10(cycles)

    if (failed == 0):
        marker = ['x', 'x']
    else:
        marker = [',', '+', '1', '*', '2', 'o']
    color = ['r', 'b', 'y', 'g', 'k', 'm']

    plt.figure(1)
    plt.grid(True)
    plt.scatter(cycles, maxStress, alpha = 0.9,
                label = file, marker = random.choice(marker),
                color= random.shuffle(color))
    plt.ylabel('Stress amplitude (MPa)')
    plt.xlabel('Number of Cycles')
    plt.title('Fatigue SN-curve')

    plt.figure(2)
    plt.grid(True)
    plt.scatter(logcycles, logmaxStress, alpha = 0.9,
                label = file, marker = random.choice(marker),
                color= random.shuffle(color))
    plt.ylabel('log(Stress amplitude)')
    plt.xlabel('log(Cycles)')
    plt.title('Fatigue log-log SN-curve')

    print("######## Data for Specimen ########")
    print(file)
    print("###################################")
    print('Max Stress = ' + str(round(max(stress), 4)) + ' MPa')
    print('Min Stress = ' + str(round(max(stress)*0.1, 4)) + ' MPa')
    print('Stress Amp = ' + str(round(maxStress, 4)) + ' MPa')
    print('Stress Mean = ' + str(round(((max(stress) + max(stress) * 0.1) / 2), 4)) + ' MPa')
    print('Num of Cycles = ' + str(int(maxCycle)) + ' Cycles')
    print("############## END ################", "\n")


# Defining global variables
data = "global"
maxCycle = "global"
maxStressList, cyclesList, logmaxStressList, logcyclesList = [], [], [], []

for files in range(0, len(file)):
    OpenFile(file[files], cycleFile[files], folder)
    plot = FCurve(L[files], W[files], T[files], data, file[files], maxCycle, failed[files])
    maxStressList.append(maxStress)
    cyclesList.append(cycles)
    print(maxStress)
    logmaxStressList.append(logmaxStress)
    logcyclesList.append(logcycles)


x = cyclesList
y = maxStressList
logx = logcyclesList
logy = logmaxStressList

order = np.argsort(x)
xs = np.array(x)[order]
ys = np.array(y)[order]

logorder = np.argsort(logx)
logxs = np.array(logx)[order]
logys = np.array(logy)[order]

# Linear Regression of SN data
z = np.polyfit(xs, ys, 1)
p = np.poly1d(z)
fit1 = p

logz = np.polyfit(logxs, logys, 1)
logp = np.poly1d(logz)
logfit1 = logp

# R SQUARE VALUE of log-log regression line
yhat = logp(logxs)
ybar = np.sum(logys) / len(logys)
ssreg = np.sum((yhat - ybar) ** 2)
sstot = np.sum((logys - ybar) ** 2)  #
r2 = ssreg / sstot
print('Regression r-square = ' + str(r2))


# Curve fit for the SN plot (log function is the best fit)
def func(x, a, b):
    return a * np.log10(x) + b

popt, pcov = curve_fit(func, xs, ys)


# Fit plot
plt.figure(1)
# plt.plot(xs, fit1(xs), "r-", alpha = 0.8)
plt.xlim(0, max(cyclesList)*1.02)
plt.ylim(min(maxStressList)*0.98, max(maxStressList)*1.02)
plt.legend(loc='upper right')
plt.plot(xs, func(xs, *popt), 'r-')

plt.figure(2)
plt.plot(logxs, logfit1(logxs), "r-", alpha = 0.8)
plt.legend(loc='upper right')
plt.xlim(min(logcyclesList)*0.98, max(logcyclesList)*1.02)
plt.ylim(min(logmaxStressList)*0.98, max(logmaxStressList)*1.02)

plt.figure(3)
sns.regplot(logxs, logys, ci= 95, color = 'black', marker='s')
plt.grid(True)
plt.ylabel('log(Stress amplitude)')
plt.xlabel('log(Cycles)')
plt.title('log-log SN-curve for ' + strgroup + ' | Regression R-Square = ' + str(round(r2, 6)))
plt.legend(["Regression line", "Specimen", "Confidence level of 95%"], loc='upper right')
plt.xlim(min(logcyclesList)*0.98, max(logcyclesList)*1.02)
plt.ylim(min(logmaxStressList)*0.98, max(logmaxStressList)*1.02)


plt.show()


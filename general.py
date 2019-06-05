###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import csv
import matplotlib.pyplot as plt
import random
import numpy as np

folder = './thermalData/'
files = ['A_thermalData', 'B_thermalData', 'C_thermalData', 'DY_thermalData', 'DBK_thermalData']

file = files[0]

def OpenFile(file):
    global data
    data = csv.reader(open(folder + file + '.csv', 'r'),
                      quoting = csv.QUOTE_NONNUMERIC,
                      delimiter = ",", quotechar = '|')
    return data

OpenFile(file)

W, T, tempInitial, tempFinal, ultForce, amp, stress, leg, t_list = [], [], [], [], [], [], [], [], []

for row in data:
    W.append(row[0])
    T.append(row[1])
    tempInitial.append(row[2])
    tempFinal.append(row[3])
    ultForce.append(row[4])
    amp.append(row[1])
    stress.append(row[4]/(row[0]*row[1]))

for i in range(0, len(stress)):
    leg.append(str(round(stress[i], 2))+" MPa")
leg = sorted(leg)

stress, tempInitial, tempFinal = sorted(stress), sorted(tempInitial), sorted(tempFinal)
for i in range(0, len(stress)):
    y = np.linspace(tempInitial[i], tempFinal[i], len(stress))
    x = np.linspace(0, stress[i], len(stress))
    color = ['r', 'b', 'y', 'g', 'k', 'm']
    plt.plot(x, y, color= random.shuffle(color), label = leg[i])
    plt.scatter(stress[i], tempFinal[i], alpha = 0.8,
                color= 'r')
    plt.scatter(0, tempInitial[i], alpha = 0.8,
                color= 'b')
#  Regression
z = np.polyfit(stress, tempFinal, 1)
p = np.poly1d(z)
fit1 = p

# Fit plot
plt.figure(1)
plt.plot(stress, fit1(stress), "r--", alpha = 0.5)

plt.xlabel('Engineering Stress (MPa)')
plt.ylabel('Temperature C')
plt.title('Temperature - Fatigue Stress')

plt.grid(True)
plt.legend(loc='lower right')

xx = [[0.003131410799892603, 725.8257841916477, 2.272858699458243, 'A'],
    [0.003757703599442227, 580.1843862267269, 2.1801609564643516, 'B'],
    [0.0024872214168683965, 716.2743641001666, 1.7815329387437262, 'C'],
    [0.0023891939640211905, 664.8877833776082, 1.5885458787972102, 'DY'],
    [0.0027270525272091615, 682.6839547568655, 1.8617150041048551, 'DBK']]

q = [0.4408223615, 0.1348238482, 0.1973831776, 0.3948339483, 0.3653433476]


x = [row[3] for row in xx]
tand = [row[0] for row in xx]
E_stor = [row[1] for row in xx]
E_loss = [row[2] for row in xx]

plt.figure(2)
plt.plot(x, tand, "b--", alpha = 0.5)
plt.plot(x, tand, "ro", alpha = 0.9)

plt.xlabel('Age group')
plt.ylabel('tan(δ)')
plt.title('Damping ratio change with age')
plt.grid(True)

plt.figure(3)
plt.plot(x, E_stor, "g--", alpha = 0.5)
plt.plot(x, E_stor, "ro", alpha = 0.9)

plt.xlabel('Age group')
plt.ylabel('Storage Modulus MPa')
plt.title('Storage Modulus change with age')
plt.grid(True)

plt.figure(4)
plt.plot(x, E_loss, "k--", alpha = 0.5)
plt.plot(x, E_loss, "ro", alpha = 0.9)

plt.xlabel('Age group')
plt.ylabel('Loss Modulus MPa')
plt.title('Loss Modulus change with age')

plt.grid(True)


plt.figure(5)
plt.plot(x, q, "k--", alpha = 0.5)
plt.plot(x, q, "ro", alpha = 0.9)

plt.xlabel('Age group')
plt.ylabel('Poisson ratio')
plt.title('Poisson ratio change with age')

plt.grid(True)

t_list = [37.9, 33.1, 37.7, 41.8, 36.1]
age = ['A', 'B', 'C', 'DY', 'DBK']

plt.figure(6), plt.plot(age, t_list, 'blue'), plt.plot(age, t_list, 'ro'), plt.grid(True)


plt.show()
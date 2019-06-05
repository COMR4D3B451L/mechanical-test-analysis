import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import csv
from numpy import polyder

# Specimen Parameters in mm (Length, Width, Thickness)

L, W, T, file = 30, 10.07, 4.83, 'A_S_Y_1_20190506'

group1 = [[30, 10.07, 4.83, 'A_S_Y_1_20190506'],
              [30, 10.17, 5.14, 'B_S_Y_3_20190506'],
              [30, 10.1, 4.71, 'C_S_BK_5_20190506'],
              [30, 10.08, 5.25, 'D_S_Y_4_20190506'],
              [30, 10.13, 4.8, 'D_S_BK_2_20190506']]

group2 = [[30, 10.06, 4.91, 'A_C1_Y_66_20190530'],
              [30, 10.14, 5.12, 'B_C1_Y_67_20190530'],
              [30, 10.17, 4.73, 'C_C1_BK_68_20190530'],
              [30, 10.13, 5.33, 'D_C1_Y_69_20190530'],
              [30, 10.07, 4.76, 'D_C1_BK_70_20190530']]

group3 = [[30, 10.07, 5.04, 'A_S_Y_71_20190530'],
              [30, 10.14, 5.12, 'B_S_Y_72_20190530'],
              [30, 10.17, 4.88, 'C_S_BK_73_20190530'],
              [30, 10.18, 5.19, 'D_S_Y_74_20190530'],
              [30, 10.11, 4.77, 'D_S_BK_75_20190530']]


# Import the test data file (Time, Force, Displacement)
data = csv.reader(open('./static/' + file + '.csv', 'r'),
                  quoting = csv.QUOTE_NONNUMERIC,
                  delimiter = ",", quotechar = '|')
# Arrays
time = []
force = []
dis = []
stress = []
strain = []
area = W*T
for row in data:
    time.append(row[0])
    force.append(row[1])
    dis.append(row[2])
    stress.append(row[1]/area)
    strain.append(((row[2]))/L)

# What data do we want to work with
x = strain
y = stress

for items in x:
    float(items)
for items in y:
    float(items)

# Degrees of polynomial regression (1 for linear regression)
degree = 12

# Polynomial Regression
z = np.polyfit(x, y, degree)
p = np.poly1d(z)

# R SQUARE VALUE
yhat = p(x)
ybar = np.sum(y) / len(y)
ssreg = np.sum((yhat - ybar) ** 2)
sstot = np.sum((y - ybar) ** 2)  #
r2 = ssreg / sstot

# Finding the index of values between 0.0004 and 0.0006
value = 0
for strn in x:
    if 0.001 <= strn <= 0.0012:
        value = strn
        break

idx05 = x.index(value)

# Finding the index of values between 0.002 and 0.003
value1 = 0
for strn1 in x:
    if 0.002 <= strn1 <= 0.003:
        value1 = strn1
idx25 = x.index(value1)

# Linear Regression2
x_linear = x[idx05:idx25]
y_linear = y[idx05:idx25]
z1 = np.polyfit(x_linear, y_linear, 1)

# Linear Regression3
x_linear2 = x[int(len(x)*0.05):int(len(x)*0.25)]
y_linear2 = y[int(len(x)*0.05):int(len(x)*0.25)]
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

# Offset line
xline = np.linspace(-100, 100, len(x))
yline = slope*(xline - 0.0025)



# plotting the main values

plt.figure(1)
plot1 = pl.plot(x, y, data=data, marker='.', color='blue')

# Plot Labels
pl.ylabel('Engineering Stress (MPa)')
pl.xlabel('Engineering Strain (mm/mm)')
pl.title('Stress-Strain curve')

# Plot borders
plt.xticks([0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.2])
plt.yticks([0, 10, 20, 30, 40, 50, 60])
plt.xlim(0, 0.2)
plt.ylim(0, 60)

# Fit plot
pl.plot(x, fit1(x), "r-")

# Diff plot
# pl.plot(x, diff_fit1(x), "y.")

# Fit2 Plot
pl.plot(x, fit2(x), "g-")

# Fit3 Plot
pl.plot(x, fit3(x), "y-")

# Plot Offset Line
# pl.plot (xline, yline, 'y-')

# plt.scatter(x1, y1)

# R Square Value of the main fit
print("r-Square for the fit = ", r2)

# Data from test
print("Ultimate Strength = ", max(y), "MPa")
print("Stress at Failure =", y[-1], "MPa")
print("Strain at Failure =", x[-1], "mm/mm")
print("Displacement at Failure =", dis[-1], "mm")
print("Young's Modulus Range:", slope, "MPa", slope2, "MPa")

# Legend and show
plt.legend(['PDCPD Data', 'Fit', 'E - ISO', 'E - Flat region slope'], )
plt.grid(True)

plt.figure(2)
plt.grid(True)
plt.plot(time, strain)

pl.show()
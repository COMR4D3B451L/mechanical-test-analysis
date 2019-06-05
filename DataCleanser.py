###########################################################################
# ################ Created By Basil Abu-Ragheef May-2019 ################ #
###########################################################################

import os
import glob
import pandas as pd

def DataCleanser(datFile):
    global df
    # Open the file
    df = pd.read_csv(datFile,
                     sep = '\t', engine = 'python', skipinitialspace = True, skiprows = 1)

    # Keywords to filter rows that contain them
    df = df[~df['Cyclic Acquisition'].isin(['Cyclic Acquisition', 'Stored at:',
                                            'Points:', 'Running Time', 's', 'Points: ', 'Stored at: '])]

    # Filter first 4 rows
    df = df[4:]

    # Change "," with "."
    df = df.apply(lambda x: x.str.replace(',', '.'))

    # Filter columns
    df = df.iloc[:, 0:5]

    return df

def DataCleanser2(datFile2):
    global df
    # Open the file
    df = pd.read_csv(datFile2,
                     sep = '\t', engine = 'python', skipinitialspace = True, skiprows = 1)
    # Keywords to filter rows that contain them
    df = df[~df['Data Acquisition'].isin(['Data Acquisition',
                                            'Running Time', 'Count'])]
    df = df.applymap(str)
    # Filter first 4 rows
    df = df[4:]

    # Change "," with "."
    df = df.apply(lambda x: x.str.replace(',', '.'))
    df = df.applymap(float)

    # Filter columns
    df = df.iloc[:, 0:5]

    return df

def DataCleanser3(datFile3):
    global df
    # Open the file
    df = pd.read_csv(datFile3,
                     sep = '\t', engine = 'python', skipinitialspace = True, skiprows = 2)
    # Keywords to filter rows that contain them
    df = df[~df['Data Acquisition'].isin(['Data Acquisition',
                                            'Running Time', 'Count', 's', 'Time:'])]
    df = df.applymap(str)
    # Filter first 4 rows
    df = df[4:]
    # Change "," with "."
    df = df.apply(lambda x: x.str.replace(',', '.'))

    # Filter columns
    df = df.iloc[:, 0:5]

    df = df.applymap(float)


    return df

def DataCleanser4(datFile4):
    global df
    # Open the file
    df = pd.read_csv(datFile4,
                     sep = '\t', engine = 'python', skipinitialspace = True, skiprows = 1)
    # Keywords to filter rows that contain them
    df = df[~df['Data Acquisition'].isin(['Data Acquisition',
                                            'Running Time', 'Count'])]
    df = df.applymap(str)
    # Filter first 4 rows
    df = df[4:]

    # Change "," with "."
    df = df.apply(lambda x: x.str.replace(',', '.'))
    df = df.applymap(float)

    # Filter columns
    df = df.iloc[:, 0:5]

    return df

# Global definitions
df = "global"
datFiles, datFiles2, datFiles3, datFiles4, fileName, fileName2, fileName3, fileName4 = [], [], [], [], [], [], [], []

# Create new input folder "dat"
indir = './datCyclicStress'
if not os.path.exists(indir):
    os.mkdir(indir)

# Create new input folder "CyclicBuffer"
indir2 = './datCyclicBufferReadout'
if not os.path.exists(indir2):
    os.mkdir(indir2)

# Create new input folder "Creep"
indir3 = './datCreep'
if not os.path.exists(indir3):
    os.mkdir(indir3)

# Create new input folder "Creep"
indir4 = './datCyclicStrainCyclicBufferReadout'
if not os.path.exists(indir4):
    os.mkdir(indir4)

# Check for files in dat
for file in os.listdir(indir):
    if file.endswith(".dat"):
        datFiles.append(os.path.join(indir, file))
        fileName.append(os.path.splitext(file)[0])

for file in os.listdir(indir2):
    if file.endswith(".dat"):
        datFiles2.append(os.path.join(indir2, file))
        fileName2.append(os.path.splitext(file)[0])

for file in os.listdir(indir3):
    if file.endswith(".dat"):
        datFiles3.append(os.path.join(indir3, file))
        fileName3.append(os.path.splitext(file)[0])

for file in os.listdir(indir4):
    if file.endswith(".dat"):
        datFiles4.append(os.path.join(indir4, file))
        fileName4.append(os.path.splitext(file)[0])

# Create new output folder "csv"
outdir = './csvCyclicStress'
if not os.path.exists(outdir):
    os.mkdir(outdir)

# Create new output folder "CyclicBuffer"
outdir2 = './csvCyclicBufferReadout'
if not os.path.exists(outdir2):
    os.mkdir(outdir2)

# Create new output folder "Creep"
outdir3 = './csvCreep'
if not os.path.exists(outdir3):
    os.mkdir(outdir3)

# Create new output folder "CyclicStrain"
outdir4 = './csvCyclicStrainCyclicBufferReadout'
if not os.path.exists(outdir4):
    os.mkdir(outdir4)

# Manage file names (csv)
filenames, files_present = [], []
for file in fileName:
    filenames.append(os.path.join(outdir, file+'.csv'))

for file in os.listdir(outdir):
    files_present.append(glob.glob(file))

for files in range(0, len(datFiles)):
    DataCleanser(datFiles[files])
    if not files_present:
        df.to_csv(filenames[files], header = False)
        print('Success! You can find your files in the csv folder', filenames[files])

    else:
        print('WARNING: This file already exists in the csv folder!', filenames[files])


# Manage file names (BufferReadout)
filenames2, files_present2 = [], []
for file in fileName2:
    filenames2.append(os.path.join(outdir2, file+'.csv'))

for file in os.listdir(outdir2):
    files_present2.append(glob.glob(file))

for files in range(0, len(datFiles2)):
    DataCleanser2(datFiles2[files])
    if not files_present2:
        df.to_csv(filenames2[files], header = False)
        print('Success! You can find your files in the BufferReadout folder', filenames2[files])

    else:
        print('WARNING: This file already exists in the BufferReadout folder!', filenames2[files])

# Manage file names (BufferReadout)
filenames3, files_present3 = [], []
for file in fileName3:
    filenames3.append(os.path.join(outdir3, file+'.csv'))

for file in os.listdir(outdir3):
    files_present3.append(glob.glob(file))

for files in range(0, len(datFiles3)):
    DataCleanser3(datFiles3[files])
    if not files_present3:
        df.to_csv(filenames3[files], header = False)
        print('Success! You can find your files in the Creep folder', filenames3[files])

    else:
        print('WARNING: This file already exists in the Creep folder!', filenames3[files])

# Manage file names (CyclicStrain)
filenames4, files_present4 = [], []
for file in fileName4:
    filenames4.append(os.path.join(outdir4, file+'.csv'))

for file in os.listdir(outdir4):
    files_present4.append(glob.glob(file))

for files in range(0, len(datFiles4)):
    DataCleanser4(datFiles4[files])
    if not files_present4:
        df.to_csv(filenames4[files], header = False)
        print('Success! You can find your files in the CyclicStrain folder', filenames4[files])

    else:
        print('WARNING: This file already exists in the CyclicStrain folder!', filenames4[files])

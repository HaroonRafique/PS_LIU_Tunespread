import os
import shutil
import numpy as np
from math import log10, floor

# Functions
########################################################################
def round_sig(x, sig=3):
        return round(x, sig-int(floor(log10(abs(x))))-1)

def replace_point_with_p(input_str):
        return input_str.replace(".", "p")
    
def is_non_zero_file(fpath):  
        print '\tis_non_zero_file:: Checking file ', fpath
        print '\tis_non_zero_file:: File exists = ', os.path.isfile(fpath)
        print '\tis_non_zero_file:: Size > 3 bytes = ', os.path.getsize(fpath)
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 3

# USER PARAMETERS
########################################################################
output_file = '/output/output.mat'
destination_folder = './Saved_Outputs/'

str_voltages = []
voltages = []
v_step = 0.1 #kV
steps = 30
for i in range(steps):
    # Middle selected as 41.8kV
    min_voltage = 41.8 - ((steps - 1)/2 * v_step)    
    rf_voltage = round_sig(min_voltage + (i*v_step),3)        
    str_voltages.append(replace_point_with_p(str(rf_voltage)))
    voltages.append(round_sig(rf_voltage*1E-3))

# Locations
########################################################################
PO_locations = []
PO_locations.append('./00_00')
PO_locations.append('./00_01')
PO_locations.append('./00_02')
PO_locations.append('./00_03')
PO_locations.append('./00_04')
PO_locations.append('./00_05')
PO_locations.append('./00_06')
PO_locations.append('./00_07')
PO_locations.append('./00_08')
PO_locations.append('./00_09')
PO_locations.append('./00_10')
PO_locations.append('./00_11')
PO_locations.append('./00_12')
PO_locations.append('./00_13')
PO_locations.append('./00_14')
PO_locations.append('./00_15')
PO_locations.append('./00_16')
PO_locations.append('./00_17')
PO_locations.append('./00_18')
PO_locations.append('./00_19')
PO_locations.append('./00_20')
PO_locations.append('./00_21')
PO_locations.append('./00_22')
PO_locations.append('./00_23')
PO_locations.append('./00_24')
PO_locations.append('./00_25')
PO_locations.append('./00_26')
PO_locations.append('./00_27')
PO_locations.append('./00_28')
PO_locations.append('./00_29')

BL_locations = []
BL_locations.append('./01_00')
BL_locations.append('./01_01')
BL_locations.append('./01_02')
BL_locations.append('./01_03')
BL_locations.append('./01_04')
BL_locations.append('./01_05')
BL_locations.append('./01_06')
BL_locations.append('./01_07')
BL_locations.append('./01_08')
BL_locations.append('./01_09')
BL_locations.append('./01_10')
BL_locations.append('./01_11')
BL_locations.append('./01_12')
BL_locations.append('./01_13')
BL_locations.append('./01_14')
BL_locations.append('./01_15')
BL_locations.append('./01_16')
BL_locations.append('./01_17')
BL_locations.append('./01_18')
BL_locations.append('./01_19')
BL_locations.append('./01_20')
BL_locations.append('./01_21')
BL_locations.append('./01_22')
BL_locations.append('./01_23')
BL_locations.append('./01_24')
BL_locations.append('./01_25')
BL_locations.append('./01_26')
BL_locations.append('./01_27')
BL_locations.append('./01_28')
BL_locations.append('./01_29')

# Copy files
########################################################################
i = 0
for loc in PO_locations:
        original = str(loc + output_file)
        destination = str(destination_folder + 'PO_' + str_voltages[i] + '_NoSC.mat')
        is_non_zero_file(original)
        newPath = shutil.copy(original, destination)    
        if is_non_zero_file(destination):
                print 'copy_outputs:: ', original, ' copied to ', destination
        else:
                print 'copy_outputs::Error:' , destination, ' destination file empty, please check'
        i = i+1

i = 0
for loc in BL_locations:
        original = str(loc + output_file)
        destination = str(destination_folder + 'BL_' + str_voltages[i] + '_NoSC.mat')
        is_non_zero_file(original)
        newPath = shutil.copy(original, destination)    
        if is_non_zero_file(destination):
                print 'copy_outputs:: ', original, ' copied to ', destination
        else:
                print 'copy_outputs::Error:' , destination, ' destination file empty, please check'
        i = i+1

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

# ~ str_voltages = []
# ~ voltages = []
# ~ v_step = 0.1 #kV
# ~ steps = 30
# ~ for i in range(steps):
    # ~ # Middle selected as 41.8kV
    # ~ min_voltage = 39 - ((steps - 1)/2 * v_step)    
    # ~ rf_voltage = round_sig(min_voltage + (i*v_step),3)        
    # ~ str_voltages.append(replace_point_with_p(str(rf_voltage)))
    # ~ voltages.append(round_sig(rf_voltage*1E-3))

# Locations
########################################################################
NoSC_locations = []
NoSC_locations.append('./00_00')
NoSC_locations.append('./00_01')
NoSC_locations.append('./00_02')
NoSC_locations.append('./00_10')
NoSC_locations.append('./00_11')
NoSC_locations.append('./00_12')

SC_locations = []
SC_locations.append('./01_00')
SC_locations.append('./01_01')
SC_locations.append('./01_02')
SC_locations.append('./01_10')
SC_locations.append('./01_11')
SC_locations.append('./01_12')

PO_V = ['41p8', '39p9', '41p8']
BL_V = ['41p8', '41p8', '43p0']
Int = ['1p6E12', '2E12']

# Copy files
########################################################################
i = 0
for loc in NoSC_locations:
        original = str(loc + output_file)
        destination = str(destination_folder + 'I_' + Int[int(loc[-2])] + '_PO_' + PO_V[int(loc[-1])] + '_BL_' + BL_V[int(loc[-1])] + '_NoSC.mat')
        is_non_zero_file(original)
        newPath = shutil.copy(original, destination)    
        if is_non_zero_file(destination):
                print 'copy_outputs:: ', original, ' copied to ', destination
        else:
                print 'copy_outputs::Error:' , destination, ' destination file empty, please check'
        i = i+1

i = 0
for loc in SC_locations:
        original = str(loc + output_file)
        destination = str(destination_folder + 'I_' + Int[int(loc[-2])] + '_PO_' + PO_V[int(loc[-1])] + '_BL_' + BL_V[int(loc[-1])] + '_SC.mat')
        is_non_zero_file(original)
        newPath = shutil.copy(original, destination)    
        if is_non_zero_file(destination):
                print 'copy_outputs:: ', original, ' copied to ', destination
        else:
                print 'copy_outputs::Error:' , destination, ' destination file empty, please check'
        i = i+1

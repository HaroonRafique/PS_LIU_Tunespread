import shutil

# Flags to select which files to copy from master to locations
########################################################################
pyorbit                 = False
simulation_parameters   = False # Not a good idea - resets all sims to master settings (arbitrary)
flat_files              = False
tune_files              = False
distn_gen               = False
tomo_files              = True
bunch_plotting          = False

# Locations of master directory and common filenames
########################################################################
master_directory        = './00_Master'
pyorbit_file            = master_directory + '/pyOrbit.py'
sim_params_file         = master_directory + '/simulation_parameters.py'
flat_file               = master_directory + '/Flat_file.madx'
tune_file               = master_directory + '/tunes.str'
distn_generator         = master_directory + '/lib/pyOrbit_GenerateInitialDistribution.py'
tomo_file               = master_directory + '/Tomo_Files/'
bunch_plotter           = master_directory + '/Plot_Tune_and_Distn_Footprints.py'

tomo_list = [
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_40p4_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_40p3_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_40p2_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_40p1_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_40p0_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p9_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p8_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p6_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p5_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p4_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p3_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p2_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p1_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_39p0_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p9_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p8_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p6_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p5_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p4_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p3_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p2_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p1_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_38p0_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_37p9_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_37p8_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_37p6_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_37p5_2023.mat',
        'PyORBIT_Tomo_file_LIU_Ramp_Up_Standard_41p8_2023.mat'

]


# Locations to copy to
########################################################################
locations = []

locations.append('./00_00')
locations.append('./00_01')
locations.append('./00_02')
locations.append('./00_03')
locations.append('./00_04')
locations.append('./00_05')
locations.append('./00_06')
locations.append('./00_07')
locations.append('./00_08')
locations.append('./00_09')
locations.append('./00_10')
locations.append('./00_11')
locations.append('./00_12')
locations.append('./00_13')
locations.append('./00_14')
locations.append('./00_15')
locations.append('./00_16')
locations.append('./00_17')
locations.append('./00_18')
locations.append('./00_19')
locations.append('./00_20')
locations.append('./00_21')
locations.append('./00_22')
locations.append('./00_23')
locations.append('./00_24')
locations.append('./00_25')
locations.append('./00_26')
locations.append('./00_27')
locations.append('./00_28')
locations.append('./00_29')

locations.append('./01_00')
locations.append('./01_01')
locations.append('./01_02')
locations.append('./01_03')
locations.append('./01_04')
locations.append('./01_05')
locations.append('./01_06')
locations.append('./01_07')
locations.append('./01_08')
locations.append('./01_09')
locations.append('./01_10')
locations.append('./01_11')
locations.append('./01_12')
locations.append('./01_13')
locations.append('./01_14')
locations.append('./01_15')
locations.append('./01_16')
locations.append('./01_17')
locations.append('./01_18')
locations.append('./01_19')
locations.append('./01_20')
locations.append('./01_21')
locations.append('./01_22')
locations.append('./01_23')
locations.append('./01_24')
locations.append('./01_25')
locations.append('./01_26')
locations.append('./01_27')
locations.append('./01_28')
locations.append('./01_29')


if pyorbit:
	for loc in locations:
		newPath = shutil.copy(pyorbit_file, loc)
		print pyorbit_file, ' copied to ', loc

if simulation_parameters:
	for loc in locations:
		newPath = shutil.copy(sim_params_file, loc)
		print sim_params_file, ' copied to ', loc

if flat_files:
	for loc in locations:
		newPath = shutil.copy(flat_file, loc)
		print flat_file, ' copied to ', loc

if tune_files:
	for loc in locations:
		newPath = shutil.copy(tune_file, loc)
		print flat_file, ' copied to ', loc

if distn_gen:
	for loc in locations:
		loc_ = loc + '/lib'
		newPath = shutil.copy(distn_generator, loc_)
		print distn_generator, ' copied to ', loc_

if tomo_files:
        for loc in locations:
                for f in tomo_list:
                        tomo_f = tomo_file + f 
                        loc_ = loc + '/Tomo_Files/'
                        newPath = shutil.copy(tomo_f, loc_)
                        print tomo_file, ' copied to ', loc_
                                               
if bunch_plotting:
	for loc in locations:
		newPath = shutil.copy(bunch_plotter, loc)
		print bunch_plotter, ' copied to ', loc


import shutil

# Flags to select which files to copy from master to locations
########################################################################
pyorbit                 = False
simulation_parameters   = False # Not a good idea - resets all sims to master settings (arbitrary)
flat_files              = False
tune_files              = False
distn_gen               = False
bunch_plotting          = False

# Locations of master directory and common filenames
########################################################################
master_directory        = './00_Master'
pyorbit_file            = master_directory + '/pyOrbit.py'
sim_params_file         = master_directory + '/simulation_parameters.py'
flat_file               = master_directory + '/Flat_file.madx'
tune_file               = master_directory + '/tunes.str'
distn_generator         = master_directory + '/lib/pyOrbit_GenerateInitialDistribution.py'
bunch_plotter           = master_directory + '/Plot_Tune_and_Distn_Footprints.py'


# Locations to copy to
########################################################################
locations = []

locations.append('/Run2_BMCS')
locations.append('/Run2_Standard')
locations.append('/Run3_Standard_2021')
locations.append('/Run3_Standard_2022')
locations.append('/Run3_Standard_2023')


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

                                               
if bunch_plotting:
	for loc in locations:
		newPath = shutil.copy(bunch_plotter, loc)
		print bunch_plotter, ' copied to ', loc


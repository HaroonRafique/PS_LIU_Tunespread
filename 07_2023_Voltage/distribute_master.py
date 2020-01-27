import shutil

pyorbit = False
simulation_parameters = True
flat_files = False
tune_files = False
distn_gen = False

master_directory = './00_Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'
flat_file = master_directory + '/Flat_file.madx'
tune_file = master_directory + '/tunes.str'
distn_generator = master_directory + '/lib/pyOrbit_GenerateInitialDistribution.py'

sbs_locations = []
noSC_locations = []

sbs_locations.append('./1/')
sbs_locations.append('./2/')
sbs_locations.append('./3/')
sbs_locations.append('./4/')
sbs_locations.append('./5/')
sbs_locations.append('./6/')
sbs_locations.append('./7/')

if pyorbit:
	for loc in sbs_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		print pyorbit_file, ' copied to ', loc

if simulation_parameters:
	for loc in sbs_locations:
		newPath = shutil.copy(sim_params_file, loc)
		print sim_params_file, ' copied to ', loc

if flat_files:
	for loc in sbs_locations:
		newPath = shutil.copy(flat_file, loc)
		print flat_file, ' copied to ', loc

if tune_files:
	for loc in sbs_locations:
		newPath = shutil.copy(tune_file, loc)
		print flat_file, ' copied to ', loc

if distn_gen:
	for loc in sbs_locations:
		loc_ = loc + 'lib/'
		newPath = shutil.copy(distn_generator, loc_)
		print distn_generator, ' copied to ', loc_

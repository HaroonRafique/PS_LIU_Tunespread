import shutil

pyorbit = True
simulation_parameters = False
flat_files = False
tune_files = False
distn_gen = True

master_directory = './00_Master/PyORBIT'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'
flat_file = master_directory + '/Flat_file.madx'
tune_file = master_directory + '/tunes.str'
distn_generator = master_directory + '/lib/pyOrbit_GenerateInitialDistribution.py'

NoSC_Scan = True
SC_Scan = True

sbs_locations = []
sbs_locations.append('./01_NoSC_PreLIU_BCMS/PyORBIT')
sbs_locations.append('./01_NoSC_PreLIU_Standard/PyORBIT')
sbs_locations.append('./01_NoSC_LIU_BCMS/PyORBIT')
sbs_locations.append('./01_NoSC_LIU_Standard/PyORBIT')
sbs_locations.append('./01_NoSC_LIU_Standard_2021/PyORBIT')
sbs_locations.append('./01_NoSC_LIU_Standard_2022/PyORBIT')
sbs_locations.append('./01_NoSC_LIU_Standard_2023/PyORBIT')

sbs_locations.append('./02_SC_PreLIU_BCMS/PyORBIT')
sbs_locations.append('./02_SC_PreLIU_Standard/PyORBIT')
sbs_locations.append('./02_SC_LIU_BCMS/PyORBIT')
sbs_locations.append('./02_SC_LIU_Standard/PyORBIT')
sbs_locations.append('./02_SC_LIU_Standard_2021/PyORBIT')
sbs_locations.append('./02_SC_LIU_Standard_2022/PyORBIT')
sbs_locations.append('./02_SC_LIU_Standard_2023/PyORBIT')

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
		loc_ = loc + '/lib'
		newPath = shutil.copy(distn_generator, loc_)
		print distn_generator, ' copied to ', loc_

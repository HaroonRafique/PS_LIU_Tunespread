import os

master_dir = os.getcwd()

locations = []

	locations.append('/01')
	locations.append('/02')
	locations.append('/03')
	locations.append('/04')
	locations.append('/05')
	locations.append('/06')
	locations.append('/07')
	locations.append('/08')
	locations.append('/09')
	locations.append('/10')
	locations.append('/11')
	locations.append('/12')
	locations.append('/13')
	locations.append('/14')
	locations.append('/15')
	locations.append('/16')
	locations.append('/17')
	locations.append('/18')
	locations.append('/19')

for loc in locations:
	print '---------------------------------------------------------------------------'
	print '\t Submitting SLURM Job: PS LIU Voltage Check Sim ', loc[-2:]
	print '---------------------------------------------------------------------------'
	dir_ = master_dir + loc
	make_command = 'python Make_SLURM_submission_script.py'
	submit_command = 'sbatch SLURM_submission_script.sh'
	os.chdir(dir_)
	os.system(make_command)
	os.system(submit_command)

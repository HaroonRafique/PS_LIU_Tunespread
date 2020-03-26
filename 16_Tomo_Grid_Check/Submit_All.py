import os

master_dir = os.getcwd()

locations = []

locations.append('/00_00')
locations.append('/00_01')
locations.append('/00_02')
locations.append('/00_10')
locations.append('/00_11')
locations.append('/00_12')

locations.append('/01_00')
locations.append('/01_01')
locations.append('/01_02')
locations.append('/01_10')
locations.append('/01_11')
locations.append('/01_12')

for loc in locations:
	print '---------------------------------------------------------------------------'
	print '\t Submitting SLURM Job: PS LIU Voltage Check Sim ', loc
	print '---------------------------------------------------------------------------'
	dir_ = master_dir + loc
	make_command = 'python Make_SLURM_submission_script.py'
	submit_command = 'sbatch SLURM_submission_script.sh'
	os.chdir(dir_)
	os.system(make_command)
	os.system(submit_command)

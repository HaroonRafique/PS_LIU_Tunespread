import os

master_dir = os.getcwd()

locations = []

# ~ locations.append('/00')
# ~ locations.append('/01')
# ~ locations.append('/02')
# ~ locations.append('/03')
# ~ locations.append('/04')
# ~ locations.append('/05')
# ~ locations.append('/06')
# ~ locations.append('/07')
# ~ locations.append('/08')
# ~ locations.append('/09')
# ~ locations.append('/10')
# ~ locations.append('/11')

locations.append('/01_00')
locations.append('/01_01')
locations.append('/01_02')
locations.append('/01_03')
locations.append('/01_04')
locations.append('/01_05')
locations.append('/01_06')
locations.append('/01_07')
locations.append('/01_08')
locations.append('/01_09')
locations.append('/01_10')

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

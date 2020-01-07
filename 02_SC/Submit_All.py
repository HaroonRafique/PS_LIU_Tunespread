import os

master_dir = os.getcwd()

locations = []
#locations.append('/01_PreLIU_Nominal')
#locations.append('/02_PreLIU_BCMS')
locations.append('/03_LIU_Nominal')
locations.append('/04_LIU_BCMS')

for loc in locations:
	print '--------------------------------------------------------------------------------------------'
	print '\t Submitting HPC-Batch LIU Tunespread simulation: ',loc,' Scan, tune (6.21, 6.245) SC'
	print '--------------------------------------------------------------------------------------------'
	dir_ = master_dir + loc
	make_command = 'python Make_SLURM_submission_script.py'
	submit_command = 'sbatch SLURM_submission_script.sh'
	os.chdir(dir_)
	os.system(make_command)
	os.system(submit_command)

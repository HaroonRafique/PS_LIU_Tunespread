import os

Scan = True

master_dir = os.getcwd()


locations = []
locations.append('/01_00')
locations.append('/01_01')

if Scan:
	for loc in locations:
		print '--------------------------------------------------------------------------------------------'
		print '\t Submitting HPC-Batch simulation:', loc
		print '--------------------------------------------------------------------------------------------'
		dir_ = master_dir + loc 
		make_command = 'python Make_SLURM_submission_script.py'
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)
		os.system(submit_command)


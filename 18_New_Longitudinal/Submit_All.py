import os

master_dir = os.getcwd()

locations = []


locations.append('/Run2_BMCS')
locations.append('/Run2_Standard')
locations.append('/Run3_BMCS')
locations.append('/Run3_Standard_2021')
locations.append('/Run3_Standard_2022')
locations.append('/Run3_Standard_2023')

for loc in locations:
	print '---------------------------------------------------------------------------'
	print '\t Submitting SLURM Job: PS Injection Sim ', loc
	print '---------------------------------------------------------------------------'
	dir_ = master_dir + loc
	make_command = 'python Make_SLURM_submission_script.py'
	submit_command = 'sbatch SLURM_submission_script.sh'
	os.chdir(dir_)
	os.system(make_command)
	os.system(submit_command)

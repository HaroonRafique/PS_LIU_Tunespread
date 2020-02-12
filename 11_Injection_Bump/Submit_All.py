import os

NoSC_Scan = True
SC_Scan = True

master_dir = os.getcwd()

NoSC_locations = []
NoSC_locations.append('/01_NoSC_PreLIU_BCMS')
NoSC_locations.append('/01_NoSC_PreLIU_Standard')
NoSC_locations.append('/01_NoSC_LIU_BCMS')
NoSC_locations.append('/01_NoSC_LIU_Standard')
NoSC_locations.append('/01_NoSC_LIU_Standard_2021')
NoSC_locations.append('/01_NoSC_LIU_Standard_2022')
NoSC_locations.append('/01_NoSC_LIU_Standard_2023')

SC_locations = []
SC_locations.append('/02_SC_PreLIU_BCMS')
SC_locations.append('/02_SC_PreLIU_Standard')
SC_locations.append('/02_SC_LIU_BCMS')
SC_locations.append('/02_SC_LIU_Standard')
SC_locations.append('/02_SC_LIU_Standard_2021')
SC_locations.append('/02_SC_LIU_Standard_2022')
SC_locations.append('/02_SC_LIU_Standard_2023')


if NoSC_Scan:
	for loc in NoSC_locations:
		print '--------------------------------------------------------------------------------------------'
		print '\t Submitting HPC-Batch simulation:', loc
		print '--------------------------------------------------------------------------------------------'
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)
		os.system(submit_command)

if SC_Scan:
	for loc in SC_locations:
		print '--------------------------------------------------------------------------------------------'
		print '\t Submitting HPC-Batch simulation:', loc
		print '--------------------------------------------------------------------------------------------'
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)
		os.system(submit_command)

